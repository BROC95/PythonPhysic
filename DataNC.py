import cdstoolbox as ct


@ct.application(title='Query data Colombia')
@ct.output.download()
def application():

    data = ct.catalogue.retrieve(
        'reanalysis-era5-single-levels',
        {
            'variable': '2m_temperature',
            'product_type': 'reanalysis',
            'year': '2017',
            'month': '01',
            'day': '01',
            'time': '12:00'
        }
    )
    mapa=ct.map.plot(data,title="MAPA")
    

    return mapa