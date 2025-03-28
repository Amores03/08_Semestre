from sklearn.preprocessing import OneHotEncoder

def EncoderMail(mail):
    prep_email = [[w] for w in mail['subject'] + mail['body']]

    enc = OneHotEncoder(handle_unknown='ignore')
    x = enc.fit_transform(prep_email)

    return enc.get_feature_names_out(), x


