import datetime
import sys
import time

import pandas as pd

import argparse
import re

from pandas import DataFrame

arg_parser = argparse.ArgumentParser(
        description="Enrich individual companies with organisational and \
         funding data. You must set input and output json file names"
)
arg_parser.add_argument(
        "--divestments", required=True, type=str
)
arg_parser.add_argument(
        "--portfolio", required=True, type=str
)
arg_parser.add_argument(
        '--organisation', required=True, type=str
)
arg_parser.add_argument(
        '--funding', required=True, type=str
)


def normalize(company_name: str):
    stripped = re.sub('[^a-zA-Z0-9 ]+', '', company_name)
    lower = stripped.lower()
    return lower


class Company():
    @staticmethod
    def columns_of_interest() -> list:
        return [

        ]

    @staticmethod
    def flatten(df: DataFrame):
        flat = pd.json_normalize(df.company_details).add_prefix('company_details.')

        print(f'flat: {flat.columns.values.tolist()}')
        print(f'flat: {flat.shape[0]}')
        r = df.join(flat)
        print(r.columns.values.tolist())
        print(f'joined: {r.columns.values.tolist()}')
        print(f'joined: {r.shape[0]}')
        return r


def process(
        portfolio: DataFrame,
        divestments: DataFrame,
        organisation: DataFrame,
        funding: DataFrame
):
    companies = pd.concat([portfolio, divestments])
    companies['normalized_company_name'] = companies['title'].apply(
            lambda company_name: normalize(company_name)).astype(str)
    organisation['normalized_company_name'] = organisation['company_name'].apply(
            lambda company_name: normalize(company_name)).astype(str)
    companies_with_org_data = companies.merge(organisation, how='left', on='normalized_company_name',
                                              suffixes=('_c', '_o'))
    companies_with_org_data.rename(columns={'uuid': 'company_uuid'}, inplace=True)

    fundings_by_company_id = funding.groupby('company_uuid').apply(list).reset_index().rename(columns={1: 'fundings'})

    companies_with_org_data_and_funding = companies_with_org_data.merge(fundings_by_company_id, how='left',
                                                                        left_on='company_uuid', right_on='company_uuid')

    print(companies.info(verbose=True, max_cols=20))
    print(organisation.info(verbose=True, max_cols=20))
    print(companies_with_org_data.info(verbose=True, max_cols=20))
    print(fundings_by_company_id.info(verbose=True, max_cols=20))
    print(companies_with_org_data_and_funding.info(verbose=True, max_cols=20))

    print('summary:')
    print(f'companies {companies.shape[0]}')
    print(f'organisation {organisation.shape[0]}')
    print(f'companies_with_org_data {companies_with_org_data.shape[0]}')
    print(f'companies_with_org_data_and_funding {companies_with_org_data_and_funding.shape[0]}')
    return companies_with_org_data_and_funding


def main(args):
    date = datetime.date.today()
    portfolio = pd.read_json(args.portfolio, lines=True)
    divestments = pd.read_json(args.divestments, lines=True)

    organisation = pd.read_json(args.organisation, lines=True, compression='gzip')

    funding = pd.read_json(args.funding, lines=True, compression='gzip')
    output = process(portfolio=portfolio, divestments=divestments, organisation=organisation, funding=funding)
    print(output.head())
    output.to_json()


if __name__ == '__main__':
    args = arg_parser.parse_args()
    main(args)
