from flask import Flask, render_template, request, redirect
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Gunakan backend non-GUI untuk server/web
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
df = pd.read_csv("financial_statement_idx.csv")
df_harga = pd.read_excel("harga_saham_20250704.xlsx")
ds = pd.read_csv("daftar_saham.csv")

class fundamental_analisis:
    def __init__(self, df, df_harga, ds):
        self.df = df
        self.df_harga = df_harga
        self.ds = ds

    def filter_symbol(self, symbol):
        self.data = self.df[self.df['symbol'] == symbol]
        self.data_harga = self.df_harga[self.df_harga['Kode Saham'] == symbol]
        self.daftar_saham = self.ds[self.ds['Kode'] == symbol]
        if (not self.data.empty) and (not self.data_harga.empty) and (not self.daftar_saham.empty):
            return self.data, self.data_harga,self.daftar_saham
        else:
            print(f"Kode Saham {symbol} Tidak Ada")
            return None

    def get_account(self, account_name):
        df_acc = self.data[self.data['account'] == account_name]
        if df_acc.empty:
            print(f"Akun {account_name} tidak ditemukan.")
            return None
        try:
            return df_acc.iloc[0][['2020', '2021', '2022', '2023']].astype(float)
        except KeyError:
            print("Kolom tahun tidak ditemukan.")
            return None
        
    def nama_perusahaan(self, symbol):
        data = self.df_harga[self.df_harga['Kode Saham'] == symbol]

        if not data.empty:
            return data.iloc[0]['Nama Perusahaan']
        else:
            return None
    def harga_saham(self, symbol):
        data = self.df_harga[self.df_harga['Kode Saham'] == symbol]

        if not data.empty:
            return data.iloc[0]['Penutupan']
        else:
            return None
    def jumlah_saham_beredar(self, symbol):
        data = self.df_harga[self.df_harga['Kode Saham'] == symbol]

        if not data.empty:
            return data.iloc[0]['Tradeble Shares']
        else:
            return None
    def jumlah_saham_keseluruhan(self, symbol):
        data = self.df_harga[self.df_harga['Kode Saham'] == symbol]

        if not data.empty:
            return data.iloc[0]['Listed Shares']
        else:
            return None
    def tanggal_listing(self, symbol):
        data = self.ds[self.ds['Kode'] == symbol]

        if not data.empty:
            return data.iloc[0]['Tanggal Pencatatan']
        else:
            return None
    def papan_pencatatan(self, symbol):
        data = self.ds[self.ds['Kode'] == symbol]

        if not data.empty:
            return data.iloc[0]['Papan Pencatatan']
        else:
            return None

    ### ANALISIS KINERJA KEUANGAN ###
    #1. Laba kotor(gross margin) %
    def gross_margin(self):
        operating_revenue = self.get_account("Operating Revenue")
        operating_expense = self.get_account("Operating Expense")

        if operating_revenue is None or operating_expense is None:
            print("Data tidak lengkap untuk menghitung gross margin.")
            return {'2020': 0, '2021': 0, '2022': 0, '2023': 0}
        
        gross_margin = {}
        for year in ['2020', '2021', '2022', '2023']:
            or_val = operating_revenue.get(year)
            oe_val = operating_expense.get(year)

            if pd.isna(or_val) or pd.isna(oe_val) or or_val == 0 or oe_val == 0:
                gross_margin[year] = 0
            else:
                gross_margin[year] = round(((or_val - oe_val) / or_val) * 100, 2)

        return gross_margin
    #2. Laba Bersih (net margin) %
    def net_margin(self):
        net_income = self.get_account("Net Income")
        total_revenue = self.get_account("Total Revenue")

        if net_income is None or total_revenue is None:
            print("Data tidak lengkap untuk menghitung net margin.")
            return {'2020': 0, '2021': 0, '2022': 0, '2023': 0}
        
        net_margin = {}
        for year in ['2020', '2021', '2022', '2023']:
            ni_val = net_income.get(year)
            tr_val = total_revenue.get(year)

            if pd.isna(ni_val) or pd.isna(tr_val) or ni_val == 0 or tr_val == 0:
                net_margin[year] = 0
            else:
                net_margin[year] = round((ni_val / tr_val)* 100, 2)

        return net_margin   
    #3. Operating Margin
    def operating_margin(self):
        operating_income = self.get_account("Operating Income")
        operating_revenue = self.get_account("Operating Revenue")

        if operating_income is None or operating_revenue is None:
            print("Data tidak lengkap untuk menghitung Operating Margin.")
            return {'2020': 0, '2021': 0, '2022': 0, '2023': 0}
        
        operating_margin = {}
        for year in ['2020', '2021', '2022', '2023']:
            om_val = operating_income.get(year)
            or_val = operating_revenue.get(year)
            
            if pd.isna(om_val) or pd.isna(or_val) or om_val == 0 or or_val == 0:
                operating_margin[year] = 0
            else:
                operating_margin[year] = round((om_val / or_val)*100, 2)

        return operating_margin 
    #4. Pendapatan bunga bersih (Net Interest Income)
    def net_interest_income(self):
        interest_income = self.get_account("Interest Income")
        interest_expense = self.get_account("Interest Expense")

        if interest_income is None or interest_expense is None:
            print("Data tidak lengkap untuk menghitung net interest income.")
            return {'2020': 0, '2021': 0, '2022': 0, '2023': 0}
        
        net_interest_income = {}
        for year in ['2020', '2021', '2022', '2023']:
            ii_val = interest_income.get(year)
            ie_val = interest_expense.get(year)

            if pd.isna(ii_val) or pd.isna(ie_val) or ii_val == 0 or ie_val == 0:
                net_interest_income[year] = 0
            else:
                net_interest_income[year] = round((ii_val - ie_val), 2)

        return net_interest_income  
    #5. EPS (Earnings Per Share) basic
    def eps_basic(self):
        net_income = self.get_account("Net Income")
        basic_avg_share = self.get_account("Basic Average Shares")

        if net_income is None or basic_avg_share is None:
            print("Data tidak lengkap untuk menghitung eps basic.")
            return {'2020': 0, '2021': 0, '2022': 0, '2023': 0}
        
        eps_basic = {}
        for year in ['2020', '2021', '2022', '2023']:
            ni_val = net_income.get(year)
            bas_val = basic_avg_share.get(year)
            
            if pd.isna(ni_val) or pd.isna(bas_val) or ni_val == 0 or bas_val == 0:
                eps_basic[year] = 0
            else:
                eps_basic[year] = round((ni_val / bas_val), 2)

        return eps_basic
    #6. EPS (Earnings Per Share) diluted
    def eps_diluted(self):
        net_income = self.get_account("Net Income")
        diluted_avg_share = self.get_account("Diluted Average Shares")
        

        if net_income is None or diluted_avg_share is None:
            print("Data tidak lengkap untuk menghitung eps diluted.")
            return {'2020': 0, '2021': 0, '2022': 0, '2023': 0}
        
        eps_diluted = {}
        for year in ['2020', '2021', '2022', '2023']:
            ni_val = net_income.get(year)
            das_val = diluted_avg_share.get(year)

            if pd.isna(ni_val) or pd.isna(das_val) or ni_val == 0 or das_val == 0:
                eps_diluted[year] = 0
            else:
                eps_diluted[year] = round((ni_val / das_val), 2)

        return eps_diluted
    
    ### ANALISIS STRUKTUR MODAL ###
    #1. Debt to Equity Ratio
    def debt_equity(self):
        total_debt = self.get_account("Total Debt")
        total_equity = self.get_account("Total Equity Gross Minority Interest")

        if total_debt is None or total_equity is None:
            print("Data tidak lengkap untuk menghitung debt to equity ratio.")
            return {'2020': 0, '2021': 0, '2022': 0, '2023': 0}
        
        debt_equity = {}
        for year in ['2020', '2021', '2022', '2023']:
            td_val = total_debt.get(year)
            te_val = total_equity.get(year)
            
            if pd.isna(td_val) or pd.isna(te_val) or te_val == 0 or td_val == 0:
                debt_equity[year] = 0
            else:
                debt_equity[year] = round((td_val / te_val), 2)

        return debt_equity 
    #2. Debt to Asset Ratio
    def debt_asset(self):
        total_debt = self.get_account("Total Debt")
        total_asset = self.get_account("Total Assets")

        if total_debt is None or total_asset is None:
            print("Data tidak lengkap untuk menghitung debt to asset ratio.")
            return {'2020': 0, '2021': 0, '2022': 0, '2023': 0}
        
        debt_asset = {}
        for year in ['2020', '2021', '2022', '2023']:
            td_val = total_debt.get(year)
            ta_val = total_asset.get(year)
            
            if pd.isna(td_val) or pd.isna(ta_val) or td_val == 0 or ta_val == 0:
                debt_asset[year] = 0
            else:
                debt_asset[year] = round((td_val / ta_val), 2)

        return debt_asset
    #3. Equity Ratio
    def equity_ratio(self):
        total_equity = self.get_account("Total Equity Gross Minority Interest")
        total_asset = self.get_account("Total Assets")

        if total_equity is None or total_asset is None:
            print("Data tidak lengkap untuk menghitung debt to asset ratio.")
            return {'2020': 0, '2021': 0, '2022': 0, '2023': 0}
        
        equity_ratio = {}
        for year in ['2020', '2021', '2022', '2023']:
            te_val = total_equity.get(year)
            ta_val = total_asset.get(year)
            
            if pd.isna(te_val) or pd.isna(ta_val) or te_val == 0 or ta_val == 0:
                equity_ratio[year] = 0
            else:
                equity_ratio[year] = round((te_val / ta_val), 2)

        return equity_ratio
    
    ### ANALISIS ARUS KAS ###
    # Free Cash Flow (FCF)
    def cash_flow(self):
        operating_cash_flow = self.get_account("Operating Cash Flow")
        capital_expenditure = self.get_account("Capital Expenditure")

        if operating_cash_flow is None or capital_expenditure is None:
            print("Data tidak lengkap untuk menghitung Free Cash Flow.")
            return {'2020': 0, '2021': 0, '2022': 0, '2023': 0}
        
        cash_flow = {}
        for year in ['2020', '2021', '2022', '2023']:
            ocf_val = operating_cash_flow.get(year)
            ce_val = capital_expenditure.get(year)
            
            if pd.isna(ocf_val) or pd.isna(ce_val) or ocf_val == 0 or ce_val == 0:
                cash_flow[year] = 0
            else:
                cash_flow[year] = round((ocf_val - ce_val), 2)

        return cash_flow
    
    ### ANALISIS EFESIENSI dan OPERASI ###
    #1. Asset Turnover
    def asset_turnover(self):
        total_revenue = self.get_account("Total Revenue")
        total_asset = self.get_account("Total Assets")

        if total_revenue is None or total_asset is None:
            print("Data tidak lengkap untuk menghitung Asset Turnover.")
            return {'2020': 0, '2021': 0, '2022': 0, '2023': 0}
        
        asset_turnover = {}
        for year in ['2020', '2021', '2022', '2023']:
            tr_val = total_revenue.get(year)
            ta_val = total_asset.get(year)
            
            if pd.isna(tr_val) or pd.isna(ta_val) or tr_val == 0 or ta_val == 0:
                asset_turnover[year] = 0
            else:
                asset_turnover[year] = round((tr_val / ta_val), 2)

        return asset_turnover  
    #2. Depreciation % of Revenue
    def depreciation_revenue(self):
        depreciation = self.get_account("Depreciation")
        operating_revenue = self.get_account("Operating Revenue")

        if depreciation is None or operating_revenue is None:
            print("Data tidak lengkap untuk menghitung Depreciation of Revenue.")
            return {'2020': 0, '2021': 0, '2022': 0, '2023': 0}
        
        depreciation_revenue = {}
        for year in ['2020', '2021', '2022', '2023']:
            d_val = depreciation.get(year)
            or_val = operating_revenue.get(year)
            
            if pd.isna(d_val) or pd.isna(or_val) or d_val == 0 or or_val == 0:
                depreciation_revenue[year] = 0
            else:
                depreciation_revenue[year] = round((d_val / or_val)*100, 2)

        return depreciation_revenue
    #3. Return on Assets (ROA)
    def roa(self):
        net_income = self.get_account("Net Income")
        total_asset = self.get_account("Total Assets")

        if net_income is None or total_asset is None:
            print("Data tidak lengkap untuk menghitung ROA.")
            return {'2020': 0, '2021': 0, '2022': 0, '2023': 0}
        
        roa = {}
        for year in ['2020', '2021', '2022', '2023']:
            ni_val = net_income.get(year)
            ta_val = total_asset.get(year)
            
            if pd.isna(ni_val) or pd.isna(ta_val) or ni_val == 0 or ta_val == 0:
                roa[year] = 0
            else:
                roa[year] = round((ni_val / ta_val), 2)

        return roa
    #4. Return on Equity (ROE)
    def roe(self):
        net_income = self.get_account("Net Income")
        total_equity = self.get_account("Total Equity")

        if net_income is None or total_equity is None:
            print("Data tidak lengkap untuk menghitung ROE.")
            return {'2020': 0, '2021': 0, '2022': 0, '2023': 0}
        
        roe = {}
        for year in ['2020', '2021', '2022', '2023']:
            ni_val = net_income.get(year)
            te_val = total_equity.get(year)
            
            if pd.isna(ni_val) or pd.isna(te_val) or ni_val == 0 or te_val == 0:
                roe[year] = 0
            else:
                roe[year] = round((ni_val / te_val), 2)

        return roe
    
    ### ANALISIS LIKUIDITAS ###
    #1. Current Ratio 
    def current_ratio(self):
        current_assets = self.get_account("Current Assets")
        current_liabilities = self.get_account("Current Liabilities")

        if current_assets is None or current_liabilities is None:
            print("Data tidak lengkap untuk menghitung Current Ratio.")
            return {'2020': 0, '2021': 0, '2022': 0, '2023': 0}
        
        current_ratio = {}
        for year in ['2020', '2021', '2022', '2023']:
            ca_val = current_assets.get(year)
            cl_val = current_liabilities.get(year)
            
            if pd.isna(ca_val) or pd.isna(cl_val) or ca_val == 0 or cl_val == 0:
                current_ratio[year] = 0
            else:
                current_ratio[year] = round((ca_val / cl_val), 2)

        return current_ratio
    #2. Cash Ratio 
    ## rumus (cash + cash_equivalents) / current_liabilities
    def cash_ratio(self):
        #cash = None
        cash_equivalents = self.get_account("Cash Equivalents")
        current_liabilities = self.get_account("Current Liabilities")

        if cash_equivalents is None or current_liabilities is None:
            print("Data tidak lengkap untuk menghitung Cash Ratio.")
            return {'2020': 0, '2021': 0, '2022': 0, '2023': 0}
        
        cash_ratio = {}
        for year in ['2020', '2021', '2022', '2023']:
            ce_val = cash_equivalents.get(year)
            cl_val = current_liabilities.get(year)
            
            if pd.isna(ce_val) or pd.isna(cl_val) or ce_val == 0 or cl_val == 0:
                cash_ratio[year] = 0
            else:
                #cash_ratio[year] = round(((cash + ce_val) / cl_val), 2)
                cash_ratio[year] = round((ce_val / cl_val), 2)

        return cash_ratio
    
    ### ANALISIS PAJAK ###
    #1. Effective Tax Rate 
    def tax_rate(self):
        tax_provision = self.get_account("Tax Provision")
        pretax_income = self.get_account("Pretax Income")

        if tax_provision is None or pretax_income is None:
            print("Data tidak lengkap untuk menghitung Effective Tax Rate")
            return {'2020': 0, '2021': 0, '2022': 0, '2023': 0}
        
        tax_rate = {}
        for year in ['2020', '2021', '2022', '2023']:
            tp_val = tax_provision.get(year)
            pi_val = pretax_income.get(year)
            
            if pd.isna(tp_val) or pd.isna(pi_val) or tp_val == 0 or pi_val == 0:
                tax_rate[year] = 0
            else:
                tax_rate[year] = round((tp_val / pi_val)* 100, 2)

        return tax_rate
    #2. Tax Effect on Unusual Items
    def tax_effect_unusual(self):
        tax_effect_of_unusual_items = self.get_account("Tax Effect Of Unusual Items")
        total_unusual_items = self.get_account("Total Unusual Items")

        if tax_effect_of_unusual_items is None or total_unusual_items is None:
            print("Data tidak lengkap untuk menghitung Tax Effect on Unusual Items.")
            return {'2020': 0, '2021': 0, '2022': 0, '2023': 0}
        
        tax_effect_unusual = {}
        for year in ['2020', '2021', '2022', '2023']:
            teu_val = tax_effect_of_unusual_items.get(year)
            tui_val = total_unusual_items.get(year)
            
            if pd.isna(teu_val) or pd.isna(tui_val) or teu_val == 0 or tui_val == 0:
                tax_effect_unusual[year] = 0
            else:
                tax_effect_unusual[year] = round((teu_val / tui_val)* 100, 2)

        return tax_effect_unusual
    
    ### ANALISIS RISIKO ###
    #1. Rasio Write Off terhadap Total Aset (Mendeteksi risiko akuntansi)
    def write_off(self):
        write_off = self.get_account("Write Off")
        total_asset = self.get_account("Total Assets")

        if write_off is None or total_asset is None:
            print("Data tidak lengkap untuk menghitung Write Off Ratio")
            return {'2020': 0, '2021': 0, '2022': 0, '2023': 0}
        
        write_off = {}
        for year in ['2020', '2021', '2022', '2023']:
            wo_val = write_off.get(year)
            ta_val = total_asset.get(year)
            
            if pd.isna(wo_val) or pd.isna(ta_val) or wo_val == 0 or ta_val == 0:
                write_off[year] = 0
            else:
                write_off[year] = round((wo_val / ta_val)* 100, 2)

        return write_off
    #2. Unusual Items as % of Revenue (Menilai kualitas laba)
    def unusual_ratio(self):
        total_unusual_items = self.get_account("Total Unusual Items")
        total_revenue = self.get_account("Total Revenue")

        if total_unusual_items is None or total_revenue is None:
            print("Data tidak lengkap untuk menghitung Current Ratio.")
            return {'2020': 0, '2021': 0, '2022': 0, '2023': 0}
        
        unusual_ratio = {}
        for year in ['2020', '2021', '2022', '2023']:
            tui_val = total_unusual_items.get(year)
            tr_val = total_revenue.get(year)
            
            if pd.isna(tui_val) or pd.isna(tr_val) or tui_val == 0 or tr_val == 0:
                unusual_ratio[year] = 0
            else:
                unusual_ratio[year] = round((tui_val / tr_val)* 100, 2)

        return unusual_ratio
    
    ### ANALISIS CAGR dan Y0Y ###
    #1. Revenue
    def revenue(self):
        total_revenue = self.get_account("Total Revenue")

        if total_revenue is None :
            print("Data Total Revenue tidak lengkap")
            return {'2020': 0, '2021': 0, '2022': 0, '2023': 0},{'CAGR': None},{'YoY': None}
        
        revenue = {}
        for year in ['2020', '2021', '2022', '2023']:
            total_revenue_val = total_revenue.get(year)
            
            if pd.isna( total_revenue_val) or  total_revenue_val == 0 :
                revenue[year] = 0
            else:
                revenue[year] = round(total_revenue_val, 2)

        tr_2020 = safe_float(total_revenue.get('2020'))
        tr_2023 = safe_float(total_revenue.get('2023'))
        tr_2022 = safe_float(total_revenue.get('2022'))

        cagr_revenue = {'CAGR': calculate_cagr(tr_2020, tr_2023)}
        yoy_revenue = {'YoY': calculate_yoy(tr_2022, tr_2023)}

        return revenue,cagr_revenue,yoy_revenue
    #2. Net Income
    def income(self):
        net_income = self.get_account("Net Income")

        if net_income is None :
            print("Data Net Income tidak lengkap")
            return {'2020': 0, '2021': 0, '2022': 0, '2023': 0},{'CAGR': None},{'YoY': None}
        
        income = {}
        for year in ['2020', '2021', '2022', '2023']:
            net_income_val = net_income.get(year)
            
            if pd.isna( net_income_val) or  net_income_val == 0 :
                income[year] = 0
            else:
                income[year] = round(net_income_val, 2)

        ni_2020 = safe_float(net_income.get('2020'))
        ni_2023 = safe_float(net_income.get('2023'))
        ni_2022 = safe_float(net_income.get('2022'))

        cagr_income = {'CAGR': calculate_cagr(ni_2020, ni_2023)}
        yoy_income = {'YoY': calculate_yoy(ni_2022, ni_2023)}

        return income,cagr_income,yoy_income
    #3. Eps Basic
    def basic(self):
        data = self.eps_basic()
        if not data:
            print("Data EPS Basic tidak tersedia")
            return {'CAGR': None},{'YoY': None}

        eps_2020 = safe_float(data.get('2020'))
        eps_2023 = safe_float(data.get('2023'))
        eps_2022 = safe_float(data.get('2022'))

        cagr_basic = {'CAGR': calculate_cagr(eps_2020, eps_2023)}
        yoy_basic = {'YoY': calculate_yoy(eps_2022, eps_2023)}

        return cagr_basic, yoy_basic
    #4. Eps Diluted
    def diluted(self):
        data = self.eps_diluted()
        if not data:
            print("Data EPS Diluted tidak tersedia")
            return {'CAGR': None},{'YoY': None}

        eps_2020 = safe_float(data.get('2020'))
        eps_2023 = safe_float(data.get('2023'))
        eps_2022 = safe_float(data.get('2022'))

        cagr_diluted = {'CAGR': calculate_cagr(eps_2020, eps_2023)}
        yoy_diluted = {'YoY': calculate_yoy(eps_2022, eps_2023)}

        return cagr_diluted, yoy_diluted
    #5. Free Cash Flow
    def free_cash_flow(self):
        free_cash = self.get_account("Free Cash Flow")

        if free_cash is None :
            print("Data free_cash_flow tidak lengkap")
            return {'2020': 0, '2021': 0, '2022': 0, '2023': 0},{'CAGR': None},{'YoY': None}
        
        free_cash_flow = {}
        for year in ['2020', '2021', '2022', '2023']:
            free_cash_val = free_cash.get(year)
            
            if pd.isna( free_cash_val) or  free_cash_val == 0 :
                free_cash_flow[year] = 0
            else:
                free_cash_flow[year] = round(free_cash_val, 2)

        eps_2020 = safe_float(free_cash.get('2020'))
        eps_2023 = safe_float(free_cash.get('2023'))
        eps_2022 = safe_float(free_cash.get('2022'))

        cagr_free_cash = {'CAGR': calculate_cagr(eps_2020, eps_2023)}
        yoy_free_cash = {'YoY': calculate_yoy(eps_2022, eps_2023)}

        return free_cash_flow,cagr_free_cash,yoy_free_cash
    
    ### ANALISIS VALUASI ###
    #1. PER (Price to Earnings Ratio)
    def per(self):
        harga_saham = safe_float(self.data_harga["Penutupan"])
        eps_dilut = self.eps_diluted()
        if eps_dilut is None:
            print("Data Eps Diluted tidak ditemukan.")
            return {'PBV': None}
        
        eps_dilut_2023 = safe_float(eps_dilut.get('2023'))

        if harga_saham is None or eps_dilut_2023 is None:
            print("Data tidak lengkap untuk menghitung PER (Price to Earnings Ratio).")
            return {'PER': None}
        
        per = {}

        if pd.isna(harga_saham) or pd.isna(eps_dilut_2023) or harga_saham == 0 or eps_dilut_2023 == 0:
            per['PER'] = 0
        else:
            per['PER'] = (harga_saham - eps_dilut_2023)

        return per
    #2. PBV (Price to Book Value)
    def pbv(self):
        harga_saham = safe_float(self.data_harga["Penutupan"])
        total_equity = self.get_account("Total Equity Gross Minority Interest")
        jumlah_saham_beredar = safe_float(self.data_harga["Tradeble Shares"])

        if total_equity is None:
            print("Data total equity tidak ditemukan.")
            return {'PBV': None}
        
        total_equity_2023 = safe_float(total_equity.get('2023'))

        if harga_saham is None or total_equity_2023 is None or jumlah_saham_beredar is None :
            print("Data tidak lengkap untuk menghitung PBV (Price to Book Value).")
            return {'PBV': None}
        
        pbv = {}

        if pd.isna(harga_saham) or pd.isna(total_equity_2023) or pd.isna(jumlah_saham_beredar) or harga_saham == 0 or total_equity_2023 == 0 or jumlah_saham_beredar == 0:
            pbv['PBV'] = 0
        else:
            nilai_pbv = (harga_saham / (total_equity_2023 / jumlah_saham_beredar))
            pbv['PBV'] = round(nilai_pbv, 2)

        return pbv
    #3. PEG Ratio (Price/Earnings to Growth)
    def peg(self):
        per_dict = self.per()
        per = safe_float(per_dict.get('PER')) if per_dict else None
        net_margin = self.net_margin()

        if per is None or net_margin is None:
            print("Data tidak lengkap untuk menghitung PEG Ratio (Price/Earnings to Growth)")
            return {'PEG': None}

        net_margin_2020 = safe_float(net_margin.get('2020'))
        net_margin_2023 = safe_float(net_margin.get('2023'))

        cagr =  calculate_cagr(net_margin_2020, net_margin_2023)
        if cagr in [0, None]:
            print("NA")
            return None
        peg = {'PEG' : round(per / cagr, 2)}

        return peg
    #4. PSR (Price to Sales Ratio)
    def psr(self):
        jumlah_saham = safe_float(self.data_harga["Listed Shares"])
        harga_saham = safe_float(self.data_harga["Penutupan"])
        total_revenue = self.get_account("Total Revenue")

        if jumlah_saham is None or harga_saham is None or total_revenue is None:
            print("Data tidak lengkap untuk menghitung PSR Ratio (Price/Earnings to Growth)")
            return {'PSR': None}

        total_revenue_2023 = safe_float(total_revenue.get('2023'))

        market_cap = jumlah_saham * harga_saham
        if market_cap in [0, None]:
            print("NA")
            return None
        psr = {'PSR' : round(market_cap / total_revenue_2023, 2)}

        return psr

###########RUMUS 
def safe_float(value):
        try:
            if value is None or str(value).upper() in [0, '-', '']:
                return None
            return float(value)
        except (ValueError, TypeError):
            return None

def calculate_cagr(start, end, years=3):
    if start in [None, 0,] or end in [None, 0]:
        return 0
    if start <= 0 or end <= 0 :
        return 0
    return round(((end / start) ** (1/years) - 1) * 100, 2)

def calculate_yoy(previous, current):
    if previous in [None, 0] or current in [None, 0]:
        return 0
    if previous <= 0 or current <= 0 :
        return 0
    return round(((current - previous) / previous) * 100, 2)

### MATPOLIB ###
def generate_plot(data_dict, title, ylabel):
    plt.figure(figsize=(9, 4))
    tahun = list(data_dict.keys())
    nilai = list(data_dict.values())
    
    colors = []
    for val in nilai:
        if val == max(nilai):
            colors.append("#0E0B54")        
        elif val == min(nilai):
            colors.append("#E95656")      
        else:
            colors.append("#0E0B54")
    plt.bar(tahun, nilai, color=colors, width=0.4)
    for x,y in zip(tahun,nilai):
        offset = (max(nilai) - min(nilai)) * 0.03
        plt.text(x, y + offset, str(y), ha='center',va='bottom', fontsize=11, color='black')
        

    plt.title(title, fontsize=15)
    plt.xlabel('Tahun')
    plt.ylabel(ylabel)
    plt.ylim(0, max(nilai) * 1.4)

    
    

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    return encoded

@app.route('/saham', methods=['POST'])
def kinerja_keuangan():
    symbol = request.form['symbol'].upper()
    analisis = fundamental_analisis(df, df_harga,ds)
    hasil = analisis.filter_symbol(symbol)
    nama_perusahaan = analisis.nama_perusahaan(symbol)
    harga_saham = analisis.harga_saham(symbol)
    jumlah_saham_beredar = analisis.jumlah_saham_beredar(symbol)
    jumlah_saham_keseluruhan = analisis.jumlah_saham_keseluruhan(symbol)
    tanggal_listing = analisis.tanggal_listing(symbol)
    papan_pencatatan = analisis.papan_pencatatan(symbol)

    # ANALISIS KINERJA KEUANGAN
    gross_margin = generate_plot(analisis.gross_margin(), "Laba kotor(gross margin) %", "Persen (%)" )
    net_margin = generate_plot(analisis.net_margin(), "Laba Bersih (net margin) %", "Persen (%)")
    operating_margin = generate_plot(analisis.operating_margin(), "Operating Margin", "Persen (%)")
    net_interest_income = generate_plot(analisis.net_interest_income(), "Pendapatan bunga bersih (Net Interest Income)", "Rupiah (Rp)")
    eps_basic = generate_plot(analisis.eps_basic(), "EPS (Earnings Per Share) basic", "Rupiah (Rp)")
    eps_diluted = generate_plot(analisis.eps_diluted(), "EPS (Earnings Per Share) diluted", "Rupiah (Rp)")

    ### ANALISIS STRUKTUR MODAL ##
    debt_equity = generate_plot(analisis.debt_equity(), "Debt to Equity Ratio", "Ratio")
    debt_asset = generate_plot(analisis.debt_asset(), "Debt to Asset Ratio", "Ratio")
    equity_ratio = generate_plot(analisis.equity_ratio(), "Equity Ratio", "Ratio")

    ### ANALISIS ARUS KAS ###
    cash_flow = generate_plot(analisis.cash_flow(), "Free Cash Flow (FCF)", "Rupiah (Rp)")

    ### ANALISIS EFESIENSI dan OPERASIONAL ###
    asset_turnover = generate_plot(analisis.asset_turnover(), "Asset Turnover", "Ratio")
    depreciation_revenue = generate_plot(analisis.depreciation_revenue(), "Depreciation of Revenue", "Persen (%)")
    roa = generate_plot(analisis.roa(), "Return on Assets (ROA)", "Persen (%)")
    roe = generate_plot(analisis.roe(), "Return on Equity (ROE)", "Persen (%)")

    ### ANALISIS LIKUIDITAS ###
    current_ratio = generate_plot(analisis.current_ratio(), "Current Ratio", "Ratio")
    cash_ratio = generate_plot(analisis.cash_ratio(), "Cash Ratio ", "Ratio")

    ### ANALISIS PAJAK ###
    tax_rate = generate_plot(analisis.tax_rate(),"Effective Tax Rate" , "Persen (%)")
    tax_effect_unusual = generate_plot(analisis.tax_effect_unusual(), "Tax Effect on Unusual Items", "Persen (%)")

    ### ANALISIS RISIKO ###
    write_off = generate_plot(analisis.write_off(), "Rasio Write Off", "Ratio")
    unusual_ratio = generate_plot(analisis.unusual_ratio(), "Unusual Items as of Revenue", "Persen (%)")

    ### ANALISIS CAGR dan Y0Y ###
    #1. Revenue
    revenue, cagr_revenue, yoy_revenue = analisis.revenue()
    revenue_plot = generate_plot(revenue, "Revenue", "Rupiah (Rp)")
    
    #2. Net Income
    income, cagr_income, yoy_income = analisis.income()
    income_plot = generate_plot(income, "Net Income", "Rupiah (Rp)")
    
    #3. Eps Basic
    cagr_basic, yoy_basic = analisis.basic()
    #4. Eps Diluted
    cagr_diluted, yoy_diluted = analisis.diluted()
    #5. Free Cash Flow
    free_cash_flow, cagr_free_cash, yoy_free_cash = analisis.free_cash_flow()
    free_cash_flow_plot = generate_plot(free_cash_flow, "Free Cash FLow", "Rupiah (Rp)")
    

    ### ANALISIS VALUASI ###
    #1. PER (Price to Earnings Ratio)
    per = analisis.per()
    #2. PBV (Price to Book Value)
    pbv = analisis.pbv()
    #3. PEG Ratio (Price/Earnings to Growth)
    peg = analisis.peg()
    #4. PSR (Price to Sales Ratio)
    psr = analisis.psr()



    return render_template('saham.html', hasil=hasil, symbol=symbol, np=nama_perusahaan, hs=harga_saham, jsb=jumlah_saham_beredar, jsk=jumlah_saham_keseluruhan, tl=tanggal_listing, pp=papan_pencatatan, gm= gross_margin, nm=net_margin, om=operating_margin, nii=net_interest_income, eb=eps_basic,ed=eps_diluted,   de=debt_equity, da=debt_asset, er=equity_ratio, cf=cash_flow, at=asset_turnover, dr=depreciation_revenue, roa=roa, roe=roe, cur=current_ratio, car=cash_ratio, tr=tax_rate,   teu=tax_effect_unusual, wo=write_off, ur=unusual_ratio, revenue=revenue_plot, cr=cagr_revenue, yr=yoy_revenue, income=income_plot, ci=cagr_income, yi=yoy_income,cb=cagr_basic, yb=yoy_basic, cd=cagr_diluted, yd=yoy_diluted, fcf=free_cash_flow_plot, cfc=cagr_free_cash, yfc=yoy_free_cash, per=per, pbv=pbv, peg=peg, psr=psr)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")
    
if __name__ == '__main__':
    app.run(debug=True)

