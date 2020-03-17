def lambda_handler(event, context):
    import boto3
    from dateutil import parser as p
    from dateutil.relativedelta import relativedelta as rd
    
    client = boto3.client('ce')
    
    #get date of interest as string from event
    today_string=event['mydate']         #format as string 'YYYY-MM-DD'
    
    #convert input date from string to date
    today_date=p.parse(today_string)
    
    #calcualte yesterdays date
    yesterday_date = (today_date + rd(days=-1))
    
    #convert yesterdays date to string
    yesterday_string= '{}-{:02}-{:02}' \
        .format(yesterday_date.year, yesterday_date.month, yesterday_date.day)

    #get spend from cost explorer api
    today_response = client.get_cost_and_usage(  
            TimePeriod={
                'Start': yesterday_string,
                'End': today_string
            },
            Granularity="DAILY",
            Metrics=[
                "UnblendedCost",
            ]
        )
        
    #return cost only from json api response
    return today_response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']