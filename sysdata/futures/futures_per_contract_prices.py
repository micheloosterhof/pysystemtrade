import pandas as pd
from sysdata.data import baseData
from sysdata.futures.contracts import futuresContract

PRICE_DATA_COLUMNS = ['OPEN', 'CLOSE', 'HIGH', 'LOW', 'SETTLE']
PRICE_DATA_COLUMNS.sort() # needed for pattern matching

class futuresContractPrices(pd.DataFrame):
    """
    Data frame in specific format containing per contract information
    """

    def __init__(self, data):

        print(data)

        data_present = list(data.columns)
        data_present.sort()

        try:
            assert data_present == PRICE_DATA_COLUMNS
        except AssertionError:
            raise Exception("futuresContractPrices has to conform to pattern")

        super().__init__(data)

        self._is_empty=False

    @classmethod
    def create_empty(futuresContractPrices):
        """
        Our graceful fail is to return an empty, but valid, dataframe
        """

        data = pd.DataFrame(columns=PRICE_DATA_COLUMNS)

        futures_contract_prices = futuresContractPrices(data)

        futures_contract_prices._is_empty = True
        return futures_contract_prices

    def empty(self):
        return

BASE_CLASS_ERROR = "You have used a base class for futures price data; you need to use a class that inherits with a specific data source"

class futuresContractPriceData(baseData):
    """
    Extends the baseData object to a data source that reads in and writes prices for specific futures contracts

    This would normally be extended further for information from a specific source eg quandl, arctic

    Access via: object.get_prices_for_instrumentCode_and_contractDate('EDOLLAR','201702']
     or object.get_prices_for_contract_object(futuresContract(....))
    """

    def __repr__(self):
        return "Individual futures contract price data - DO NOT USE"

    def __getitem__(self, contract_tuple):
        """
        convenience method to get the price, make it look like a dict

        """

        instrument_code, contract_date = contract_tuple
        return self.get_prices_for_instrument_code_and_contract_date(instrument_code, contract_date)


    def contracts_with_price_data_for_instrument_code(self, instrument_code):
        raise NotImplementedError(BASE_CLASS_ERROR)

    def has_data_for_instrument_code_and_contract_date(self, instrument_code, contract_date):
        """
        Convenience method for when we have a code and date str, and don't want to build an object

        :return: data
        """

        contract_object = self._object_given_instrumentCode_and_contractDate(instrument_code, contract_date)

        return self.has_data_for_contract(contract_object)


    def has_data_for_contract(self, contract_object):

        contract_date = contract_object.date
        instrument_code = contract_object.instrument_code

        if contract_date in self.contracts_with_price_data_for_instrument_code(instrument_code):
            return True
        else:
            return False


    def _object_given_instrumentCode_and_contractDate(self, instrument_code, contract_date):
        """
        Quickly go from eg "EDOLLAR" "201801" to an object

        :param instrument_code: str
        :param contract_date: str
        :return: futuresContract
        """

        contract_object = futuresContract.simple(instrument_code, contract_date)

        return contract_object


    def get_prices_for_instrument_code_and_contract_date(self, instrument_code, contract_date):
        """
        Convenience method for when we have a code and date str, and don't want to build an object

        :return: data
        """

        contract_object = self._object_given_instrumentCode_and_contractDate(instrument_code, contract_date)

        return self.get_prices_for_contract_object(contract_object)

    def get_prices_for_contract_object(self, contract_object):
        """
        get some prices

        :param contract_object:  futuresContract
        :return: data
        """

        if self.has_data_for_contract(contract_object):
            return self._get_prices_for_contract_object_no_checking(contract_object)
        else:
            return futuresContractPrices.create_empty()


    def _get_prices_for_contract_object_no_checking(self, contract_object):
        """
        get some prices

        :param contract_object:  futuresContract
        :return: data
        """

        raise NotImplementedError(BASE_CLASS_ERROR)

    def write_prices_for_contract_object(self, futures_contract_object, futures_price_data):
        """
        Write some prices

        We don't check to see if we've already written some, since overwriting is okay.

        :param futures_contract_object:
        :param futures_price_data:
        :return: None
        """
        raise NotImplementedError(BASE_CLASS_ERROR)

    def delete_prices_for_contract_object(self, futures_contract_object, areyousure=False):
        """

        :param futures_contract_object:
        :return:
        """

        if not areyousure:
            raise Exception("You have to be sure to delete prices_for_contract_object!")

        if self.has_data_for_contract(futures_contract_object):
            self._delete_prices_for_contract_object_with_no_checks_be_careful(futures_contract_object)
        else:
            self.log.warn("Tried to delete non existent contract")

    def _delete_prices_for_contract_object_with_no_checks_be_careful(self, futures_contract_object):
        raise NotImplementedError(BASE_CLASS_ERROR)


class dictFuturesContractPrices(dict):
    """
    A dict of futures contract prices

    Keys are contract_objects

    We can use standard dict methods, but convenience methods are included
    """
    pass

