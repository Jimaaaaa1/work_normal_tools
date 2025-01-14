class CustomModel(NamedTuple):
    """
       A named tuple that can be used to initialize a custom PyTorch model.

       Args:
        name: The name of the custom model. Default is 'default_model'.
        model: The PyTorch model object which is a subclass of `torch.nn.Module` and implements the `forward` method and output a tensor of shape (batch_size x features). Alternatively, a __call__ method is also accepted.. Default is None.
        transform: A function that transforms a PIL.Image object into a PyTorch tensor that will be applied to each image before being fed to the model. Should correspond to the preprocessing logic of the supplied model. Default is None.
    """
    name: str = DEFAULT_MODEL_NAME
    model: Optional[torch.nn.Module] = None
    transform: Optional[Callable[[Image], torch.tensor]] = None

class ViT(torch.nn.Module):
    transform = ViT_B_16_Weights.IMAGENET1K_SWAG_E2E_V1.transforms()
    name = 'vit_b_16'

    def __init__(self) -> None:
        """
        Initialize a ViT model, takes mean of the final encoder layer outputs and returns those as features for a given image.
        """
        super().__init__()
        self.model = vit_b_16(weights='ViT_B_16_Weights.IMAGENET1K_SWAG_E2E_V1').eval()
        self.hidden_dim = 768 # Value inferred from here: https://github.com/pytorch/vision/blob/af048198f87da11f344ffba37d6962aa78b36218/torchvision/models/vision_transformer.py#L641
        self.patch_size = 16
        self.image_size = 384 # https://github.com/pytorch/vision/blob/af048198f87da11f344ffba37d6962aa78b36218/torchvision/models/vision_transformer.py#L378
        self.class_token = nn.Parameter(torch.zeros(1, 1, self.hidden_dim))

    def _process_input(self, x: torch.Tensor) -> torch.Tensor:
        n, c, h, w = x.shape
        p = self.patch_size
        torch._assert(h == self.image_size, f"Wrong image height! Expected {self.image_size} but got {h}!")
        torch._assert(w == self.image_size, f"Wrong image width! Expected {self.image_size} but got {w}!")
        n_h = h // p
        n_w = w // p

        # (n, c, h, w) -> (n, hidden_dim, n_h, n_w)
        x = self.model.conv_proj(x)
        # (n, hidden_dim, n_h, n_w) -> (n, hidden_dim, (n_h * n_w))
        x = x.reshape(n, self.hidden_dim, n_h * n_w)

        # (n, hidden_dim, (n_h * n_w)) -> (n, (n_h * n_w), hidden_dim)
        # The self attention layer expects inputs in the format (N, S, E)
        # where S is the source sequence length, N is the batch size, E is the
        # embedding dimension
        x = x.permute(0, 2, 1)

        return x

    def forward(self, x) -> torch.tensor:
        x = self._process_input(x)
        n = x.shape[0]

        # Expand the class token to the full batch
        batch_class_token = self.class_token.expand(n, -1, -1)
        x = torch.cat([batch_class_token, x], dim=1)
        x = self.model.encoder(x)

        # mean of all encoder outputs, performs better than the classifier "token" as used by standard language
        # architectures
        x = x.mean(dim=1)
        return x


class EfficientNet(torch.nn.Module):
    transform = EfficientNet_B4_Weights.IMAGENET1K_V1.transforms()
    name = 'efficientnet_b4'

    def __init__(self) -> None:
        """
        Initializes an EfficientNet model, cuts it at the global average pooling layer and returns the output features.
        """
        super().__init__()
        self.effnet_b4 = models.efficientnet_b4(weights='EfficientNet_B4_Weights.IMAGENET1K_V1').eval()

    def forward(self, x) -> torch.tensor:
        x = self.effnet_b4.features(x)
        x = self.effnet_b4.avgpool(x)
        return x.squeeze(dim=3).squeeze(dim=2)


if __name__ == '__main__':
    model = CustomModel(name=ViT.name,
                        model=ViT(),
                        transform=ViT.transform)