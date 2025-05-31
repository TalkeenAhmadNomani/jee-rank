def create_status_column(df, rank, opening_down_limit=None):
    def get_status(row):
        try:
            or_val = float(row['OR'])
            cr_val = float(row['CR'])
            if (rank - 300) <= cr_val < rank:
                return 'Aspirational'
            elif or_val <= rank <= cr_val:
                return 'Fitting'
            elif or_val > rank and (opening_down_limit is None or or_val <= rank + opening_down_limit):
                return 'Opening Down'
        except:
            return None
    return df.apply(get_status, axis=1)
