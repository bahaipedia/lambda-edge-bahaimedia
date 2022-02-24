# lambda-edge-detect-origin
Capture users country of origin and redirect their requests to the s3 bucket closest to them

In our setup Cloudfront sits in front of user media requests. We host a number of large files which are not 
requested frequently, consequently our miss rate can be high and Cloudfront must request the file from the 
origin s3 bucket. For users who are geographically far from the origin bucket download times can be noticably 
slow. Our Cloudfront distributon has 5 origins. This function analyizes a users country of origin in order to
signal which origin bucket Cloudfront should use in the case of a cache miss.

See also, repository lambda-edge-file-redirect which captures edge cases and returns an otherwise 'missing' file.
