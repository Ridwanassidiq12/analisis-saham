# analisis-saham

aplikasi ini dibuat dengan flask,html,css adapun librarynya pandas,matplotlib io dan base64
aplikasi ini dibuat untuk tujuan bagi investor saham yang mau menganalisis fundamental perusahaan ada pun fitur fitur didalam aplikasi ini sebagai berikut :

1. ANALISIS KINERJA KEUANGAN
Metrik ini digunakan untuk mengevaluasi kesehatan finansial perusahaan dari sisi keuntungan yang diperoleh.
Laba Kotor (Gross Margin) (%): Mengukur persentase laba kotor dibandingkan dengan pendapatan total. Ini memberikan gambaran tentang seberapa efisien perusahaan dalam menghasilkan keuntungan setelah biaya langsung produksi.
Fungsi: analisis.gross_margin()
Visualisasi: generate_plot()

Laba Bersih (Net Margin) (%): Mengukur laba bersih dibandingkan dengan pendapatan, menunjukkan persentase keuntungan bersih yang dihasilkan perusahaan dari setiap unit penjualan.
Fungsi: analisis.net_margin()
Visualisasi: generate_plot()

Operating Margin: Mengukur persentase laba operasi terhadap pendapatan. Ini menggambarkan efektivitas perusahaan dalam mengelola biaya operasional.
Fungsi: analisis.operating_margin()
Visualisasi: generate_plot()

Pendapatan Bunga Bersih (Net Interest Income): Mengukur pendapatan perusahaan dari bunga yang diterima dikurangi bunga yang dibayar.
Fungsi: analisis.net_interest_income()
Visualisasi: generate_plot()

EPS (Earnings Per Share) - Basic dan Diluted: Mengukur laba per lembar saham. EPS basic mengukur laba berdasarkan jumlah saham yang beredar, sementara EPS diluted memperhitungkan potensi saham tambahan yang dapat diterbitkan.
Fungsi: analisis.eps_basic() dan analisis.eps_diluted()
Visualisasi: generate_plot()

2. ANALISIS STRUKTUR MODAL
Analisis ini mengevaluasi struktur pendanaan perusahaan dan seberapa banyak perusahaan bergantung pada utang untuk mendanai asetnya.
Debt to Equity Ratio: Rasio antara utang dan ekuitas perusahaan. Ini mengukur seberapa banyak perusahaan dibiayai oleh utang dibandingkan dengan ekuitas pemegang saham.
Fungsi: analisis.debt_equity()
Visualisasi: generate_plot()

Debt to Asset Ratio: Rasio antara utang dan total aset, memberikan gambaran tentang proporsi aset yang dibiayai dengan utang.
Fungsi: analisis.debt_asset()
Visualisasi: generate_plot()

Equity Ratio: Mengukur persentase aset yang dibiayai oleh ekuitas pemegang saham, menunjukkan stabilitas keuangan perusahaan.
Fungsi: analisis.equity_ratio()
Visualisasi: generate_plot()

3. ANALISIS ARUS KAS
Analisis ini berfokus pada aliran kas perusahaan, yang penting untuk menilai kemampuan perusahaan dalam menghasilkan kas yang cukup untuk menjalankan operasional.
Free Cash Flow (FCF): Mengukur kas yang tersedia setelah perusahaan membayar pengeluaran untuk investasi dan pemeliharaan aset.
Fungsi: analisis.cash_flow()
Visualisasi: generate_plot()

5. ANALISIS EFISIENSI dan OPERASIONAL
Metrik ini digunakan untuk mengevaluasi efisiensi perusahaan dalam mengelola aset dan operasionalnya.
Asset Turnover: Mengukur seberapa efektif perusahaan menggunakan aset untuk menghasilkan pendapatan.
Fungsi: analisis.asset_turnover()
Visualisasi: generate_plot()

Depreciation of Revenue: Mengukur seberapa besar depresiasi yang terjadi dalam hubungan dengan pendapatan.
Fungsi: analisis.depreciation_revenue()
Visualisasi: generate_plot()

Return on Assets (ROA): Mengukur seberapa efektif perusahaan menggunakan aset untuk menghasilkan keuntungan.
Fungsi: analisis.roa()
Visualisasi: generate_plot()

Return on Equity (ROE): Mengukur seberapa efektif perusahaan menghasilkan laba dari setiap unit ekuitas yang diinvestasikan.
Fungsi: analisis.roe()
Visualisasi: generate_plot()

5. ANALISIS LIKUIDITAS
Metrik likuiditas menunjukkan kemampuan perusahaan untuk memenuhi kewajiban jangka pendeknya.
Current Ratio: Rasio yang mengukur kemampuan perusahaan untuk membayar kewajiban jangka pendek dengan aset lancarnya.
Fungsi: analisis.current_ratio()
Visualisasi: generate_plot()

Cash Ratio: Mengukur kemampuan perusahaan untuk membayar kewajiban jangka pendek menggunakan kas dan setara kas.
Fungsi: analisis.cash_ratio()
Visualisasi: generate_plot()

6. ANALISIS PAJAK
Analisis ini mengukur bagaimana perusahaan mengelola kewajiban pajaknya
Effective Tax Rate: Persentase pajak yang dibayar perusahaan terhadap laba yang dikenakan pajak.
Fungsi: analisis.tax_rate()
Visualisasi: generate_plot()

Tax Effect on Unusual Items: Mengukur pengaruh pajak terhadap item-item yang tidak biasa dalam laporan keuangan.
Fungsi: analisis.tax_effect_unusual()
Visualisasi: generate_plot()

7. ANALISIS RISIKO
Menilai seberapa besar risiko yang dihadapi perusahaan dalam pengelolaan aset dan liabilitasnya.
Write Off Ratio: Mengukur rasio kerugian yang dihapuskan terhadap total aset atau pendapatan.
Fungsi: analisis.write_off()
Visualisasi: generate_plot()

Unusual Items as Revenue: Mengukur pengaruh item yang tidak biasa terhadap pendapatan.
Fungsi: analisis.unusual_ratio()
Visualisasi: generate_plot()

8. ANALISIS CAGR dan YOY
Metrik ini digunakan untuk menilai pertumbuhan tahunan yang konsisten.
CAGR (Compound Annual Growth Rate): Mengukur tingkat pertumbuhan rata-rata tahunan suatu variabel selama periode waktu tertentu.
Fungsi: Tersedia untuk Revenue, Net Income, EPS Basic, EPS Diluted, dan Free Cash Flow.
Visualisasi: generate_plot()

YoY (Year on Year): Membandingkan hasil antara tahun berjalan dan tahun sebelumnya untuk mengukur pertumbuhan tahunan.
Fungsi: Tersedia untuk Revenue, Net Income, EPS Basic, EPS Diluted, dan Free Cash Flow.
Visualisasi: generate_plot()

9. ANALISIS VALUASI
Valuasi perusahaan mengukur sejauh mana harga pasar perusahaan mencerminkan kinerjanya.
PER (Price to Earnings Ratio): Mengukur harga saham relatif terhadap laba bersih perusahaan. Rasio ini menunjukkan seberapa mahal atau murah perusahaan untuk dibeli relatif terhadap laba yang dihasilkan.
Fungsi: analisis.per()

PBV (Price to Book Value): Mengukur harga saham relatif terhadap nilai buku per saham. Ini menunjukkan seberapa banyak investor bersedia membayar untuk setiap nilai buku perusahaan.
Fungsi: analisis.pbv()

PEG (Price/Earnings to Growth): Mengukur hubungan antara rasio harga/laba dan tingkat pertumbuhannya.
Fungsi: analisis.peg()

PSR (Price to Sales Ratio): Mengukur hubungan antara harga pasar saham dan pendapatan perusahaan.
Fungsi: analisis.psr()
