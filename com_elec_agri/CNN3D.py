import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models


class CNN3D(nn.Module):
    def __init__(self, input_channels, output_channels):
        super(CNN3D, self).__init__()

        self.input_channels = input_channels
        self.output_channels = output_channels
        self.vgg16 = models.vgg16(pretrained=True)
    
     # Encoder layers

        self.encoder_conv_00 = nn.Sequential(*[nn.Conv2d(in_channels=self.input_channels,out_channels=64,kernel_size=3,padding=1),nn.BatchNorm2d(64)])
        self.encoder_conv_01 = nn.Sequential(*[nn.Conv2d(in_channels=64,out_channels=64,kernel_size=3,padding=1),nn.BatchNorm2d(64)])

        self.encoder_conv_10 = nn.Sequential(*[nn.Conv2d(in_channels=64,out_channels=128,kernel_size=3,padding=1),nn.BatchNorm2d(128)])
        self.encoder_conv_11 = nn.Sequential(*[nn.Conv2d(in_channels=128,out_channels=128,kernel_size=3,padding=1),nn.BatchNorm2d(128)])

        self.encoder_conv_20 = nn.Sequential(*[nn.Conv2d(in_channels=128,out_channels=256,kernel_size=3,padding=1),nn.BatchNorm2d(256)])
        self.encoder_conv_21 = nn.Sequential(*[nn.Conv2d(in_channels=256,out_channels=256,kernel_size=3,padding=1),nn.BatchNorm2d(256)])
        self.encoder_conv_22 = nn.Sequential(*[nn.Conv2d(in_channels=256,out_channels=256,kernel_size=3,padding=1),nn.BatchNorm2d(256)])

        self.encoder_conv_30 = nn.Sequential(*[nn.Conv2d(in_channels=256,out_channels=512,kernel_size=3,padding=1),nn.BatchNorm2d(512)])
        self.encoder_conv_31 = nn.Sequential(*[nn.Conv2d(in_channels=512,out_channels=512,kernel_size=3,padding=1),nn.BatchNorm2d(512)])
        self.encoder_conv_32 = nn.Sequential(*[nn.Conv2d(in_channels=512,out_channels=512,kernel_size=3,padding=1),nn.BatchNorm2d(512)])

        self.encoder_conv_40 = nn.Sequential(*[nn.Conv2d(in_channels=512,out_channels=512,kernel_size=3,padding=1),nn.BatchNorm2d(512)])
        self.encoder_conv_41 = nn.Sequential(*[nn.Conv2d(in_channels=512,out_channels=512,kernel_size=3,padding=1),nn.BatchNorm2d(512)])
        self.encoder_conv_42 = nn.Sequential(*[nn.Conv2d(in_channels=512,out_channels=512,kernel_size=3,padding=1),nn.BatchNorm2d(512)])

        self.init_vgg_weigts()

        # Decoder layers

        self.decoder_convtr_42 = nn.Sequential(*[nn.ConvTranspose2d(in_channels=512,out_channels=512,kernel_size=3,padding=1),nn.BatchNorm2d(512)])
        self.decoder_convtr_41 = nn.Sequential(*[nn.ConvTranspose2d(in_channels=512,out_channels=512,kernel_size=3,padding=1),nn.BatchNorm2d(512)])
        self.decoder_convtr_40 = nn.Sequential(*[nn.ConvTranspose2d(in_channels=512,out_channels=512,kernel_size=3,padding=1),nn.BatchNorm2d(512)])

        self.decoder_convtr_32 = nn.Sequential(*[nn.ConvTranspose2d(in_channels=512,out_channels=512,kernel_size=3,padding=1),nn.BatchNorm2d(512)])
        self.decoder_convtr_31 = nn.Sequential(*[nn.ConvTranspose2d(in_channels=512,out_channels=512,kernel_size=3,padding=1),nn.BatchNorm2d(512)])
        self.decoder_convtr_30 = nn.Sequential(*[nn.ConvTranspose2d(in_channels=512,out_channels=256,kernel_size=3,padding=1),nn.BatchNorm2d(256)])

        self.decoder_convtr_22 = nn.Sequential(*[nn.ConvTranspose2d(in_channels=256,out_channels=256,kernel_size=3,padding=1),nn.BatchNorm2d(256)])
        self.decoder_convtr_21 = nn.Sequential(*[nn.ConvTranspose2d(in_channels=256,out_channels=256,kernel_size=3,padding=1),nn.BatchNorm2d(256)])
        self.decoder_convtr_20 = nn.Sequential(*[nn.ConvTranspose2d(in_channels=256,out_channels=128,kernel_size=3,padding=1),nn.BatchNorm2d(128)])

        self.decoder_convtr_11 = nn.Sequential(*[nn.ConvTranspose2d(in_channels=128,out_channels=128,kernel_size=3,padding=1),nn.BatchNorm2d(128)])
        self.decoder_convtr_10 = nn.Sequential(*[nn.ConvTranspose2d(in_channels=128,out_channels=64,kernel_size=3,padding=1),nn.BatchNorm2d(64)])

        self.decoder_convtr_01 = nn.Sequential(*[nn.ConvTranspose2d(in_channels=64,out_channels=64,kernel_size=3,padding=1),nn.BatchNorm2d(64)])
        self.decoder_convtr_00 = nn.Sequential(*[nn.ConvTranspose2d(in_channels=64,out_channels=self.output_channels,kernel_size=3,padding=1)])


    def forward(self, input_img):
        # Encoder Stage - 1
        dim_0 = input_img.size()
        x_00 = F.relu(self.encoder_conv_00(input_img))
        x_01 = F.relu(self.encoder_conv_01(x_00))
        x_0, indices_0 = F.max_pool2d(x_01, kernel_size=2, stride=2, return_indices=True)
        # Encoder Stage - 2
        dim_1 = x_0.size()
        x_10 = F.relu(self.encoder_conv_10(x_0))
        x_11 = F.relu(self.encoder_conv_11(x_10))
        x_1, indices_1 = F.max_pool2d(x_11, kernel_size=2, stride=2, return_indices=True)
        # Encoder Stage - 3
        dim_2 = x_1.size()
        x_20 = F.relu(self.encoder_conv_20(x_1))
        x_21 = F.relu(self.encoder_conv_21(x_20))
        x_22 = F.relu(self.encoder_conv_22(x_21))
        x_2, indices_2 = F.max_pool2d(x_22, kernel_size=2, stride=2, return_indices=True)
        # Encoder Stage - 4
        dim_3 = x_2.size()
        x_30 = F.relu(self.encoder_conv_30(x_2))
        x_31 = F.relu(self.encoder_conv_31(x_30))
        x_32 = F.relu(self.encoder_conv_32(x_31))
        x_3, indices_3 = F.max_pool2d(x_32, kernel_size=2, stride=2, return_indices=True)
        
        # Encoder Stage - 5
        dim_4 = x_3.size()
        x_40 = F.relu(self.encoder_conv_40(x_3))
        x_41 = F.relu(self.encoder_conv_41(x_40))
        x_42 = F.relu(self.encoder_conv_42(x_41))
        x_4, indices_4 = F.max_pool2d(x_42, kernel_size=2, stride=2, return_indices=True)
        
        # Decoder


        # Decoder Stage - 5
        x_4d = F.max_unpool2d(x_4, indices_4, kernel_size=2, stride=2, output_size=dim_4)
        x_42d = F.relu(self.decoder_convtr_42(x_4d))
        x_41d = F.relu(self.decoder_convtr_41(x_42d))
        x_40d = F.relu(self.decoder_convtr_40(x_41d))

        x_40d = x_40d + x_3

        # Decoder Stage - 4
        x_3d = F.max_unpool2d(x_40d, indices_3, kernel_size=2, stride=2, output_size=dim_3)
        x_32d = F.relu(self.decoder_convtr_32(x_3d))
        x_31d = F.relu(self.decoder_convtr_31(x_32d))
        x_30d = F.relu(self.decoder_convtr_30(x_31d))

        x_30d = x_30d + x_2

        # Decoder Stage - 3
        x_2d = F.max_unpool2d(x_30d, indices_2, kernel_size=2, stride=2, output_size=dim_2)
        x_22d = F.relu(self.decoder_convtr_22(x_2d))
        x_21d = F.relu(self.decoder_convtr_21(x_22d))
        x_20d = F.relu(self.decoder_convtr_20(x_21d))

        x_20d = x_20d + x_1

        # Decoder Stage - 2
        x_1d = F.max_unpool2d(x_20d, indices_1, kernel_size=2, stride=2, output_size=dim_1)
        x_11d = F.relu(self.decoder_convtr_11(x_1d))
        x_10d = F.relu(self.decoder_convtr_10(x_11d))


        x_10d = x_10d + x_0

        # Decoder Stage - 1
        x_0d = F.max_unpool2d(x_10d, indices_0, kernel_size=2, stride=2, output_size=dim_0)

        x_01d = F.relu(self.decoder_convtr_01(x_0d))
        x_00d = self.decoder_convtr_00(x_01d)


        return x_00d

    def init_vgg_weigts(self):
        
        self.encoder_conv_00[0].weight.data = self.vgg16.features[0].weight.data
        self.encoder_conv_00[0].bias.data = self.vgg16.features[0].bias.data
        self.encoder_conv_01[0].weight.data = self.vgg16.features[2].weight.data
        self.encoder_conv_01[0].bias.data = self.vgg16.features[2].bias.data

        
        self.encoder_conv_10[0].weight.data = self.vgg16.features[5].weight.data
        self.encoder_conv_10[0].bias.data = self.vgg16.features[5].bias.data
        self.encoder_conv_11[0].weight.data = self.vgg16.features[7].weight.data
        self.encoder_conv_11[0].bias.data = self.vgg16.features[7].bias.data

        
        self.encoder_conv_20[0].weight.data = self.vgg16.features[10].weight.data
        self.encoder_conv_20[0].bias.data = self.vgg16.features[10].bias.data
        self.encoder_conv_21[0].weight.data = self.vgg16.features[12].weight.data
        self.encoder_conv_21[0].bias.data = self.vgg16.features[12].bias.data
        self.encoder_conv_22[0].weight.data = self.vgg16.features[14].weight.data
        self.encoder_conv_22[0].bias.data = self.vgg16.features[14].bias.data

        
        self.encoder_conv_30[0].weight.data = self.vgg16.features[17].weight.data
        self.encoder_conv_30[0].bias.data = self.vgg16.features[17].bias.data   
        self.encoder_conv_31[0].weight.data = self.vgg16.features[19].weight.data
        self.encoder_conv_31[0].bias.data = self.vgg16.features[19].bias.data       
        self.encoder_conv_32[0].weight.data = self.vgg16.features[21].weight.data
        self.encoder_conv_32[0].bias.data = self.vgg16.features[21].bias.data
 
        self.encoder_conv_40[0].weight.data = self.vgg16.features[24].weight.data        
        self.encoder_conv_40[0].bias.data = self.vgg16.features[24].bias.data      
        self.encoder_conv_41[0].weight.data = self.vgg16.features[26].weight.data
        self.encoder_conv_41[0].bias.data = self.vgg16.features[26].bias.data
        self.encoder_conv_42[0].weight.data = self.vgg16.features[28].weight.data
        self.encoder_conv_42[0].bias.data = self.vgg16.features[28].bias.data