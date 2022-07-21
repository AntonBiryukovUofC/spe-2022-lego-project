#install.packages("remotes")
#remotes::install_github("ryantimpe/brickr")
library(png)
library(brickr)
library(rjson)

################################################################################


MEI <- readPNG("MEI.png")
params <- fromJSON(file="params.json")
MEI_mosaic <- image_to_mosaic(MEI, img_size = params$img_size, color_palette = params$color_palette, method=params$method, use_bricks=params$use_bricks)


## save mosaic to PNG
png("MEI_Mosaic.png")
build_mosaic(MEI_mosaic)
dev.off()

## save mosaic table to CSV
MEI_table <- MEI_mosaic$ID_bricks
write.csv(MEI_table, "MEI_table.csv", row.names=F)
## save lego pieces to CSV
MEI_pieces <- MEI_mosaic$pieces[,-2]
write.csv(MEI_pieces, "MEI_pieces.csv", row.names=F)

#table(MEI_mosaic$pieces$Brick_size)



