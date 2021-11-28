## The third eye

This project is meant to help prepare training data (masks and bounding boxes) for images gathered from copernicus 
sentinel 1 and sentinel 2 missions.

### Tasks left to implement

- [x] Create tif images from RGB bands (2, 3, 4)
- [x] Create tif segmentation masks from geospatial data from PostGis
- [x] Split tif images and masks to smaller images of size 255x255 for training data 
- [x] Create automatic script for sentinel band raster downloading and building cropping
- [x] Crop tif images and masks by min/max coordinates from geospatial ESPG:4236 data
- [ ] Refactor notebooks for better readability 
