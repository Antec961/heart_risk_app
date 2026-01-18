def pred(df):

    binaries = ['Stress Level',
                'Physical Activity Days Per Week']
    bools = ['Diabetes',
             'Family History',
             'Smoking', 'Obesity',
             'Alcohol Consumption',
             'Previous Heart Problems',
             'Medication Use']

    df = df.set_index('id').sort_index()

    df = df.drop(columns=['Unnamed: 0', 'Income', 'Troponin'])
    df.loc[:, binaries] = df.loc[:, binaries].fillna(0)
    df.loc[:, bools] = df.loc[:, bools].fillna(0)
    df.loc[:, binaries] = df.loc[:, binaries].astype('int')
    df.loc[:, bools] = df.loc[:, bools].astype('int')
    df['Gender'] = df['Gender'].replace('1.0', 'Male')
    df['Gender'] = df['Gender'].replace('0.0', 'Female')

    return df
