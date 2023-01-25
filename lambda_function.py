import pycountry_convert as conv

def lambda_handler(event, context):
    request = event['Records'][0]['cf']['request']

    '''
    This blueprint demonstrates how an origin-request trigger can be used to
    change the origin from which the content is fetched, based on request properties.
    In this example, we use the value of the CloudFront-Viewer-Country header
    to update the S3 bucket domain name to a bucket in a Region that is closer to
    the viewer.

    This can be useful in several ways:
        1) Reduces latencies when the Region specified is nearer to the viewer’s
            country.
        2) Provides data sovereignty by making sure that data is served from an
            origin that’s in the same country that the request came from.

    NOTE: 1. You must configure your distribution to cache based on the
            CloudFront-Viewer-Country header. For more information, see
            http://docs.aws.amazon.com/console/cloudfront/cache-on-selected-headers
        2. CloudFront adds the CloudFront-Viewer-Country header after the viewer
            request event. To use this example, you must create a trigger for the
            origin request event.
    '''

    continentToRegion = {
        'EU': 'eu-central-1',
        'AF': 'eu-central-1',
        'NA': 'us-east-1',
        'SA': 'sa-east-1',        
        'AS': 'ap-southeast-1',        
        'OC': 'ap-southeast-1',
        'AN': 'ap-southeast-1'
    }
    continentToDomain = {
        'EU': 'bahaimedia-eu.s3.eu-central-1.amazonaws.com',
        'AF': 'bahaimedia-eu.s3.eu-central-1.amazonaws.com',
        'NA': 'bahaimedia.s3.us-east-1.amazonaws.com',
        'SA': 'bahaimedia-sp.s3-sa-east-1.amazonaws.com',        
        'AS': 'bahaimedia-sg.s3.ap-southeast-1.amazonaws.com',        
        'OC': 'bahaimedia-sg.s3.ap-southeast-1.amazonaws.com',
        'AN': 'bahaimedia-sg.s3.ap-southeast-1.amazonaws.com'
    }

    viewerCountry = request['headers'].get('cloudfront-viewer-country')    
    if viewerCountry:
        countryCode = viewerCountry[0]['value']        
        try:
            continent = conv.country_alpha2_to_continent_code(countryCode)
        except:    
            print(f'Failed to detect region from {countryCode}, will use "continentToDomain" and "continentToRegion" methods')
            domainName = 'bahaimedia.s3.us-east-1.amazonaws.com'
            region = 'us-east-1'
        else:
            domainName = continentToDomain.get(continent)
            region = continentToRegion.get(continent)        
        
        # If the viewer's country in not in the list you specify, the request
        # goes to the default S3 bucket you've configured
        if domainName:            
            '''
            If you’ve set up OAI, the bucket policy in the destination bucket
            should allow the OAI GetObject operation, as configured by default
            for an S3 origin with OAI. Another requirement with OAI is to provide
            the Region so it can be used for the SIGV4 signature. Otherwise, the
            Region is not required.
            '''            
            request['origin']['s3']['region'] = region
            request['origin']['s3']['domainName'] = domainName
            request['headers']['host'] = [{'key': 'host', 'value': domainName}]
    return request
