import sys
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


#
# def normalize(name: str):
#     stripped = re.sub('[^a-zA-Z0-9 ]+', '', name)
#     lower = name.lower()
#     lower.strip()


class Portfolio():
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
    print(f'portf: {portfolio.columns.values.tolist()}')
    print(f'portf: {portfolio.shape[0]}')

    print(f'divestments {divestments.columns.values.tolist()}')
    print(f'divestments {divestments.shape[0]}')
    companies = pd.concat([portfolio, divestments])
    print(f'companies {companies.columns.values.tolist()}')
    print(f'companies {companies.shape[0]}')
    companies_flat = Portfolio.flatten(companies)
    return companies_flat


def main(args):
    portfolio = pd.read_json(args.portfolio, lines=True)
    divestments = pd.read_json(args.divestments, lines=True)

    organisation = None  # pd.read_json(args.organisation, lines=True, compression='gzip')

    funding = None  # pd.read_json(args.funding, lines=True, compression='gzip')
    process(portfolio=portfolio, divestments=divestments, organisation=organisation, funding=funding)


if __name__ == '__main__':
    args = arg_parser.parse_args()
    main(args)
