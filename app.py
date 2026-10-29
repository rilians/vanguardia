import io
import sqlite3
from datetime import date, timedelta

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Vanguardia — Marketing Intelligence", page_icon="◈", layout="wide", initial_sidebar_state="expanded")

PURPLE = '#7357ee'
DAYS = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']

st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');
html,body,[class*="css"], .stApp {font-family:'DM Sans', sans-serif; color:#242438;}
.stApp {background:#f7f7fb;}
.block-container {padding: 2.1rem 3.1rem 4rem; max-width: 1650px;}
header[data-testid="stHeader"] {background:transparent;}
[data-testid="stSidebar"] {background:#17162b; border-right:0;}
[data-testid="stSidebar"] * {color:#e9e7f7;}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {font-size:13px;}
[data-testid="stSidebar"] label {font-size:12px!important; font-weight:600!important; color:#c5c2db!important;}
[data-testid="stSidebar"] [data-baseweb="select"] * {color:#25243a;}
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {background:#27263d; border:1px dashed #5e5b77; border-radius:12px;}
[data-testid="stSidebar"] button {border-radius:8px;}
[data-testid="stSidebar"] hr {border-color:#37354e; margin:1.25rem 0;}
.brand {display:flex; align-items:center; gap:11px; margin:0 0 29px;}
.brand-icon {width:37px;height:37px;border-radius:11px;background:linear-gradient(135deg,#9d8bff,#7256e9);display:flex;align-items:center;justify-content:center;font-size:21px;font-weight:800;color:white;}
.brand-name {font-family:'Plus Jakarta Sans';font-weight:800;letter-spacing:-.8px;font-size:20px;color:#fff;}
.brand-sub {font-size:9px;letter-spacing:1.5px;color:#9693af;font-weight:700;margin-top:1px;}
.side-label {font-size:10px;color:#88859f!important;letter-spacing:1.6px;font-weight:700;margin:20px 0 12px;}
.side-active {background:#34304f;border-radius:9px;padding:11px 13px;color:#fff;font-size:13px;font-weight:700;border-left:3px solid #a998ff;}
.side-note {border:1px solid #403d5b;border-radius:11px;padding:13px;color:#b5b2cc;font-size:11px;line-height:1.6;}
.eyebrow {font-size:10px;letter-spacing:1.6px;font-weight:800;color:#8b88a4;margin-bottom:7px;}
.page-title {font-family:'Plus Jakarta Sans';font-size:31px;line-height:1.2;font-weight:800;letter-spacing:-1.3px;color:#211f36;margin:0 0 7px;}
.subtitle {font-size:13px;color:#8b899c;margin-bottom:4px;}
.pill {display:inline-flex;align-items:center;gap:7px;border:1px solid #e5e3ee;background:white;border-radius:99px;padding:7px 12px;font-size:11px;color:#77758c;font-weight:700;float:right;}
.dot {width:7px;height:7px;background:#50c89b;border-radius:50%;display:inline-block;}
.section-title {font-family:'Plus Jakarta Sans';font-size:15px;font-weight:800;color:#28263c;letter-spacing:-.3px;margin-bottom:3px;}
.section-sub {font-size:11px;color:#a09eaf;line-height:1.5;}
.metric-card {background:#fff;border:1px solid #edeaf4;border-radius:14px;padding:19px 20px 16px;min-height:135px;box-shadow:0 4px 18px rgba(44,35,95,.025);}
.metric-top {display:flex;justify-content:space-between;align-items:center;color:#89869a;font-size:11px;font-weight:700;}
.metric-icon {background:#f4f1ff;color:#8069e9;border-radius:9px;width:30px;height:30px;text-align:center;line-height:30px;font-size:15px;}
.metric-value {font-family:'Plus Jakarta Sans';font-size:26px;font-weight:800;color:#242238;letter-spacing:-1px;margin-top:9px;}
.metric-foot {font-size:10px;color:#9b99aa;margin-top:6px;}
.metric-foot b {color:#7257df;font-weight:700;}
.insight {background:linear-gradient(115deg,#eeeaff,#f8f6ff 66%,#f2f9f6);border:1px solid #e2dcff;border-radius:14px;padding:20px 23px;margin:20px 0 10px;}
.insight-head {font-size:10px;letter-spacing:1.3px;font-weight:800;color:#725add;margin-bottom:8px;}
.insight-title {font-family:'Plus Jakarta Sans';font-size:16px;font-weight:800;color:#292440;margin-bottom:5px;}
.insight-text {font-size:12px;color:#75718c;line-height:1.6;}
.chart-card {background:white;border:1px solid #edeaf4;border-radius:14px;padding:19px 20px 3px;}
.tag {display:inline-block;background:#eeeaff;color:#725add;border-radius:6px;padding:4px 7px;font-size:10px;font-weight:700;}
.rec {background:#fff;border:1px solid #edeaf4;border-radius:13px;padding:17px 18px;min-height:125px;}
.rec-num {color:#8a75ee;font-size:10px;font-weight:800;letter-spacing:1px;}
.rec-title {font-family:'Plus Jakarta Sans';font-size:13px;font-weight:800;margin:8px 0 6px;color:#29273f;}
.rec-text {font-size:11px;color:#8c899e;line-height:1.6;}
.small-note {font-size:11px;color:#9a98aa;line-height:1.6;}
[data-testid="stDataFrame"] {border:1px solid #edeaf4;border-radius:12px;overflow:hidden;}
[data-testid="stPlotlyChart"] {background:#fff;border:1px solid #edeaf4;border-radius:14px;padding:5px;}
div[data-testid="stDownloadButton"] button {border-radius:9px;font-size:12px;}
#MainMenu {visibility:hidden;} footer {visibility:hidden;}
@media(max-width:768px){.block-container{padding:1rem 1rem 3rem}.page-title{font-size:25px}.pill{float:none;margin-bottom:10px}}
</style>''', unsafe_allow_html=True)

ALIASES = {
    'tanggal': ['tanggal','date','posting_date','post_date','published_at','waktu','timestamp','datetime'],
    'jenis_konten': ['jenis_konten','content_type','tipe_konten','jenis konten','tipe konten','format','content'],
    'channel': ['channel','platform','kanal','media'],
    'clicks': ['clicks','klik','click','click_count'],
    'orders': ['orders','order','pesanan','konversi','conversions','conversion','jumlah_order'],
    'impressions': ['impressions','impresi','tayangan','views'],
    'spend': ['spend','biaya','cost','ad_spend','pengeluaran'],
    'revenue': ['revenue','pendapatan','omzet','sales'],
    'jam': ['jam','hour','posting_hour','post_time','waktu_posting'],
}

def make_demo():
    rng = np.random.default_rng(14)
    end = pd.Timestamp(date.today())
    rows = []
    types = ['Video pendek', 'Carousel', 'Single image', 'Story']
    channels = ['Instagram', 'TikTok', 'Facebook']
    # One row represents one post or campaign observation.
    for i in range(250):
        dt = (end - pd.Timedelta(days=int(rng.integers(0, 180)))).replace(hour=int(rng.choice([9, 10, 12, 15, 18, 19, 20, 21])), minute=int(rng.choice([0, 15, 30, 45])))
        typ = rng.choice(types, p=[.32,.27,.22,.19]); channel = rng.choice(channels, p=[.47,.33,.20])
        impressions = int(rng.integers(2500, 23000)); clicks = max(1, int(impressions * rng.uniform(.018,.075)))
        rate = {'Video pendek':.089,'Carousel':.072,'Single image':.053,'Story':.061}[typ] * (1.13 if dt.hour in [18,19,20,21] else .93)
        orders = int(rng.binomial(clicks, rate)); spend = int(rng.integers(120, 1200))*1000
        revenue = int(orders * rng.uniform(90000, 155000))
        rows.append([dt,typ,channel,impressions,clicks,orders,spend,revenue])
    return pd.DataFrame(rows, columns=['tanggal','jenis_konten','channel','impressions','clicks','orders','spend','revenue']).sort_values('tanggal')

@st.cache_data
def demo_csv():
    return make_demo().to_csv(index=False).encode('utf-8-sig')

def normalize(raw):
    raw = raw.copy()
    raw.columns = [str(c).strip().lower().replace('-', '_') for c in raw.columns]
    mapping = {}
    for canonical, choices in ALIASES.items():
        for a in choices:
            if a in raw.columns and a not in mapping:
                mapping[a] = canonical; break
    df = raw.rename(columns=mapping)
    required = ['tanggal','jenis_konten','clicks','orders']
    missing = [x for x in required if x not in df.columns]
    if missing: raise ValueError('Kolom wajib tidak ditemukan: ' + ', '.join(missing))
    df['tanggal'] = pd.to_datetime(df['tanggal'], errors='coerce', dayfirst=True, format='mixed')
    if 'jam' in df.columns:
        # A separate jam column overrides time embedded in tanggal when recognizable.
        hours = df['jam'].astype(str).str.extract(r'^(\d{1,2})(?::\d{1,2})?')[0]
        hours = pd.to_numeric(hours, errors='coerce').where(lambda x: x.between(0,23))
        mask = hours.notna() & df['tanggal'].notna()
        df.loc[mask, 'tanggal'] = df.loc[mask, 'tanggal'].dt.normalize() + pd.to_timedelta(hours[mask], unit='h')
    for col in ['clicks','orders','impressions','spend','revenue']:
        if col not in df: df[col] = 0
        df[col] = pd.to_numeric(df[col], errors='coerce')
    if 'channel' not in df: df['channel'] = 'Tidak diketahui'
    for col in ['jenis_konten','channel']:
        df[col] = df[col].fillna('Tidak diketahui').astype(str).str.strip().replace('', 'Tidak diketahui')
    initial = len(df)
    valid = df['tanggal'].notna() & df[['clicks','orders','impressions','spend','revenue']].notna().all(axis=1)
    valid &= (df[['clicks','orders','impressions','spend','revenue']] >= 0).all(axis=1)
    valid &= (df['orders'] <= df['clicks'])
    valid &= (df['clicks'] % 1 == 0) & (df['orders'] % 1 == 0)
    df = df.loc[valid, ['tanggal','jenis_konten','channel','impressions','clicks','orders','spend','revenue']].copy()
    if df.empty: raise ValueError('Tidak ada baris valid. Periksa tanggal dan angka; orders harus ≤ clicks.')
    return df, initial-len(df)

def read_upload(file):
    if file.name.lower().endswith('.csv'):
        return pd.read_csv(file, sep=None, engine='python')
    return pd.read_excel(file)

def wilson(success, n):
    if not n: return (0., 0.)
    z=1.96; p=success/n; den=1+z*z/n
    mid=(p+z*z/(2*n))/den; half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return max(0,mid-half), min(1,mid+half)

def num(x):
    if x >= 1_000_000: return f'{x/1_000_000:.1f}M'.replace('.', ',')
    if x >= 1000: return f'{x/1000:.1f}K'.replace('.', ',')
    return f'{int(x):,}'.replace(',', '.')

def pct(x): return f'{x*100:.2f}%'.replace('.', ',')
def shortdate(x): return f'{x.day} {MONTHS[x.month-1]} {x.year}'
def safe(s):
    import html
    return html.escape(str(s))

def plot_style(fig, height=300):
    fig.update_layout(height=height, margin=dict(l=15,r=15,t=32,b=10), paper_bgcolor='white',plot_bgcolor='white',font=dict(family='DM Sans, sans-serif',color='#8e8b9f',size=10), showlegend=False, xaxis=dict(showgrid=False,zeroline=False),yaxis=dict(gridcolor='#f1eff6',zeroline=False), hoverlabel=dict(bgcolor='#25233a',font_color='white'))
    return fig

def section(title, sub):
    st.markdown(f'<div class="section-title">{title}</div><div class="section-sub">{sub}</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="brand"><div class="brand-icon">◈</div><div><div class="brand-name">vanguardia</div><div class="brand-sub">MARKETING INTELLIGENCE</div></div></div><div class="side-label">WORKSPACE</div><div class="side-active">◫ &nbsp; Overview</div><div class="side-label">SUMBER DATA</div>',unsafe_allow_html=True)
    uploaded = st.file_uploader('Upload data kampanye', type=['csv','xlsx','xls'], help='Kolom wajib: tanggal, jenis_konten, clicks, orders. Kolom opsional: channel, impressions, spend, revenue, jam.')
    st.download_button('↓ Unduh contoh CSV',demo_csv(),'vanguardia_contoh.csv','text/csv',use_container_width=True)
    st.markdown('<div class="side-note">✦ &nbsp; <b>Data Anda, insight Anda.</b><br>Upload file untuk mengganti data demo. Data diproses dalam sesi aplikasi.</div>',unsafe_allow_html=True)

try:
    if uploaded:
        data, dropped = normalize(read_upload(uploaded)); source = 'Data Anda'
    else:
        data, dropped = normalize(make_demo()); source = 'Data demo'
except Exception as e:
    st.error(f'File belum dapat diproses: {e}')
    st.info('Gunakan contoh CSV sebagai acuan. Wajib: tanggal, jenis_konten, clicks, orders. Orders tidak boleh lebih besar dari clicks.')
    st.stop()
if dropped:
    st.warning(f'{dropped} baris tidak valid diabaikan (tanggal/angka kosong, angka negatif, clicks/orders bukan bilangan bulat, atau orders melebihi clicks).')

with st.sidebar:
    st.markdown('---<div class="side-label">FILTER DATA</div>',unsafe_allow_html=True)
    min_date, max_date = data['tanggal'].min().date(), data['tanggal'].max().date()
    default_start = max(min_date, max_date - timedelta(days=89))
    dates = st.date_input('Rentang tanggal', value=(default_start, max_date), min_value=min_date, max_value=max_date, format='DD/MM/YYYY')
    channels = sorted(data['channel'].unique().tolist())
    selected_channels = st.multiselect('Channel', channels, default=channels, placeholder='Pilih channel')
    types = sorted(data['jenis_konten'].unique().tolist())
    selected_types = st.multiselect('Jenis konten', types, default=types, placeholder='Pilih jenis konten')
    st.markdown('---<div class="side-label">TENTANG DASHBOARD</div><div class="side-note">Conversion rate = orders ÷ clicks. Rekomendasi bersifat observasional, bukan bukti sebab-akibat.</div>',unsafe_allow_html=True)

if len(dates) != 2:
    st.info('Pilih tanggal awal dan akhir untuk menampilkan dashboard.'); st.stop()
if not selected_channels or not selected_types:
    st.info('Pilih setidaknya satu channel dan jenis konten pada filter.'); st.stop()

# Query filtering with SQLite: all uploaded data stays in memory for this run.
conn=sqlite3.connect(':memory:')
to_sql=data.copy(); to_sql['tanggal']=to_sql['tanggal'].dt.strftime('%Y-%m-%d %H:%M:%S'); to_sql.to_sql('campaigns',conn,index=False,if_exists='replace')
q=f"SELECT * FROM campaigns WHERE date(tanggal) BETWEEN ? AND ? AND channel IN ({','.join('?'*len(selected_channels))}) AND jenis_konten IN ({','.join('?'*len(selected_types))})"
df=pd.read_sql_query(q,conn,params=[str(dates[0]),str(dates[1]),*selected_channels,*selected_types],parse_dates=['tanggal']); conn.close()
if df.empty:
    st.warning('Tidak ada data untuk kombinasi filter ini. Coba perluas rentang tanggal atau filter.'); st.stop()

clicks=df.clicks.sum(); orders=df.orders.sum(); impressions=df.impressions.sum(); rate=orders/clicks if clicks else 0
agg=df.groupby('jenis_konten',as_index=False).agg(clicks=('clicks','sum'),orders=('orders','sum'),posts=('tanggal','size'))
agg['rate']=np.where(agg.clicks>0,agg.orders/agg.clicks,0)
agg['lo'],agg['hi'] = zip(*[wilson(o,c) for o,c in zip(agg.orders,agg.clicks)])
ranked=agg[agg.clicks>0].sort_values('rate',ascending=False)
eligible=ranked[(ranked.clicks>=100)&(ranked.orders>=20)]
best=(eligible if not eligible.empty else ranked).iloc[0] if not ranked.empty else None

left,right=st.columns([4,1])
with left:
    st.markdown('<div class="eyebrow">CAMPAIGN INTELLIGENCE &nbsp; / &nbsp; OVERVIEW</div><div class="page-title">Marketing Overview</div><div class="subtitle">Pantau performa, temukan pola, dan ambil keputusan lebih cerdas.</div>', unsafe_allow_html=True)
with right:
    st.markdown(f'<div class="pill"><span class="dot"></span> {source} &nbsp; · &nbsp; {len(df)} baris</div>',unsafe_allow_html=True)
st.markdown(f'<div style="height:22px"></div><div style="display:flex;justify-content:space-between;align-items:end;margin-bottom:13px"><div><div class="section-title">Ringkasan performa</div><div class="section-sub">Gambaran kampanye pada periode terpilih</div></div><div class="tag">◷ &nbsp; {shortdate(dates[0])} – {shortdate(dates[1])}</div></div>',unsafe_allow_html=True)
metrics=[('Total impressions',num(impressions),'◉','Jumlah tayangan'),('Total clicks',num(clicks),'↗','Klik dari seluruh konten'),('Total orders',num(orders),'▣','Pesanan dari kampanye'),('Conversion rate',pct(rate) if clicks else '—','✦','Orders ÷ clicks' if clicks else 'Tidak ada clicks')]
cols=st.columns(4)
for col,(name,value,icon,desc) in zip(cols,metrics):
    col.markdown(f'<div class="metric-card"><div class="metric-top">{name}<span class="metric-icon">{icon}</span></div><div class="metric-value">{value}</div><div class="metric-foot">{desc} <b>↗</b></div></div>',unsafe_allow_html=True)

if best is not None:
    evidence='sampel memadai untuk pemantauan' if best.clicks>=100 and best.orders>=20 else 'sampel terbatas; interpretasikan dengan hati-hati'
    comparison = ''
    if len(eligible) >= 2:
        runner = eligible.iloc[1]
        diff = best.rate - runner.rate
        # Newcombe interval for the difference of two independent proportions.
        diff_lo = diff - np.sqrt((best.rate-best.lo)**2 + (runner.hi-runner.rate)**2)
        diff_hi = diff + np.sqrt((best.hi-best.rate)**2 + (runner.rate-runner.lo)**2)
        support = 'mendukung perbedaan positif dalam analisis eksploratif' if diff_lo > 0 else 'belum cukup untuk memastikan perbedaan'
        comparison = f' Dibanding {safe(runner.jenis_konten)} ({pct(runner.rate)}), selisihnya {diff*100:.2f} poin persentase (interval 95% {diff_lo*100:.2f} hingga {diff_hi*100:.2f}); data {support}.'
    st.markdown(f'<div class="insight"><div class="insight-head">✦ &nbsp; INSIGHT UTAMA</div><div class="insight-title">{safe(best.jenis_konten)} mencatat conversion rate {pct(best.rate)}</div><div class="insight-text">{int(best.orders):,} orders dari {int(best.clicks):,} clicks. Interval Wilson 95%: {pct(best.lo)}–{pct(best.hi)}; {evidence}.{comparison} Hasil ini observasional, bukan bukti sebab-akibat.</div></div>',unsafe_allow_html=True)
else:
    st.info('Belum ada clicks untuk menghitung conversion rate dan insight konten.')

st.markdown('<div style="height:16px"></div>',unsafe_allow_html=True)
a,b=st.columns([1.05,1],gap='medium')
with a:
    section('Performa jenis konten','Conversion rate berdasarkan total orders dan clicks')
    chart=agg.sort_values('rate',ascending=True)
    fig=go.Figure(go.Bar(x=chart.rate*100,y=chart.jenis_konten,orientation='h',marker=dict(color=[PURPLE if best is not None and x==best.jenis_konten else '#dcd5fb' for x in chart.jenis_konten],cornerradius=5),text=[pct(x) if c else '—' for x,c in zip(chart.rate,chart.clicks)],textposition='outside',cliponaxis=False,customdata=np.stack([chart.orders,chart.clicks],axis=-1),hovertemplate='%{y}<br>Conversion: %{x:.2f}%<br>Orders: %{customdata[0]:,.0f}<br>Clicks: %{customdata[1]:,.0f}<extra></extra>'))
    plot_style(fig,300); fig.update_xaxes(ticksuffix='%',range=[0,max(1,chart.rate.max()*125)]); fig.update_yaxes(automargin=True)
    st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
with b:
    section('Tren orders','Perkembangan pesanan dari waktu ke waktu')
    daily=df.assign(hari=df.tanggal.dt.normalize()).groupby('hari').orders.sum()
    daily=daily.reindex(pd.date_range(dates[0],dates[1],freq='D'),fill_value=0).rename_axis('hari').reset_index(name='orders')
    # Aggregate long periods for legibility, while preserving total orders.
    if len(daily)>120:
        daily=daily.set_index('hari').resample('W-MON',label='left',closed='left').sum().reset_index()
        st.caption('Ditampilkan per minggu untuk rentang lebih dari 120 hari.')
    fig=go.Figure(go.Scatter(x=daily.hari,y=daily.orders,mode='lines',line=dict(color=PURPLE,width=2.5),fill='tozeroy',fillcolor='rgba(115,87,238,0.10)',hovertemplate='%{x|%d %b %Y}<br>%{y:,.0f} orders<extra></extra>'))
    plot_style(fig,300); fig.update_yaxes(title=None); st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})

st.markdown('<div style="height:18px"></div>',unsafe_allow_html=True)
a,b=st.columns([1.05,1],gap='medium')
with a:
    section('Waktu posting terbaik','Conversion rate per hari & jam posting · warna lebih gelap = lebih tinggi')
    temp=df.copy(); temp['day']=temp.tanggal.dt.dayofweek; temp['hour']=temp.tanggal.dt.hour
    heat=temp.groupby(['day','hour']).agg(orders=('orders','sum'),clicks=('clicks','sum')).reset_index()
    heat['rate']=np.where(heat.clicks>0,heat.orders/heat.clicks*100,np.nan)
    pivot=heat.pivot(index='day',columns='hour',values='rate').reindex(index=range(7),columns=range(24))
    click_pivot=heat.pivot(index='day',columns='hour',values='clicks').reindex(index=range(7),columns=range(24))
    fig=go.Figure(go.Heatmap(z=pivot.values,x=[f'{x:02d}:00' for x in range(24)],y=DAYS,customdata=click_pivot.values,colorscale=[[0,'#f3efff'],[1,'#7659ec']],hoverongaps=False,hovertemplate='%{y}, %{x}<br>Conversion: %{z:.2f}%<br>Clicks: %{customdata:,.0f}<extra></extra>',colorbar=dict(title='%',thickness=8,len=.7),xgap=2,ygap=2))
    plot_style(fig,300); fig.update_layout(yaxis=dict(autorange='reversed',showgrid=False),xaxis=dict(tickmode='array',tickvals=[f'{x:02d}:00' for x in range(0,24,3)])); st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
    st.markdown('<div class="small-note">Sel kosong berarti tidak ada clicks. Waktu mengikuti zona waktu di file; data tanpa jam dibaca sebagai 00:00.</div>',unsafe_allow_html=True)
with b:
    section('Analisis konten','Urutkan dan bandingkan berdasarkan data teragregasi')
    table=agg.sort_values('rate',ascending=False).copy()
    table['Conversion rate']=[pct(r) if c else '—' for r,c in zip(table.rate,table.clicks)]
    table['Interval 95%']=[f'{pct(lo)} – {pct(hi)}' if c else '—' for lo,hi,c in zip(table.lo,table.hi,table.clicks)]
    table=table.rename(columns={'jenis_konten':'Jenis konten','posts':'Baris','clicks':'Clicks','orders':'Orders'})[['Jenis konten','Baris','Clicks','Orders','Conversion rate','Interval 95%']]
    st.dataframe(table,hide_index=True,use_container_width=True,height=300)
    st.markdown('<div class="small-note">Interval Wilson adalah estimasi ketidakpastian proporsi; mengasumsikan clicks independen. Data pengunjung berulang dapat membuat interval terlalu sempit.</div>',unsafe_allow_html=True)

st.markdown('<div style="height:26px"></div>',unsafe_allow_html=True)
section('Rekomendasi untuk Anda','Langkah berikutnya, berdasarkan data dan filter yang dipilih')
st.markdown('<div style="height:10px"></div>',unsafe_allow_html=True)
r1,r2,r3=st.columns(3)
with r1:
    if best is None: title='Kumpulkan data klik'; text='Tambahkan clicks dan orders untuk mulai membandingkan efektivitas konten.'
    else: title=f'Uji lebih lanjut: {safe(best.jenis_konten)}'; text=f'Format ini mencapai {pct(best.rate)} dari {int(best.clicks):,} clicks. Uji ulang pada audiens dan anggaran yang sebanding sebelum menambah investasi.'
    st.markdown(f'<div class="rec"><div class="rec-num">01 &nbsp; / &nbsp; KONTEN</div><div class="rec-title">{title}</div><div class="rec-text">{text}</div></div>',unsafe_allow_html=True)
with r2:
    reliable=heat[(heat.clicks>=100)&(heat.orders>=20)].sort_values('rate',ascending=False)
    if len(reliable):
        top=reliable.iloc[0]; title=f'Uji {DAYS[int(top.day)]}, {int(top.hour):02d}:00'; text=f'Slot ini menghasilkan {top.rate:.2f}% dari {int(top.clicks):,} clicks. Bandingkan dalam eksperimen terkontrol; perbedaan audiens dapat memengaruhi hasil.'
    else: title='Perbanyak data waktu'; text='Belum ada slot dengan minimal 100 clicks dan 20 orders. Kumpulkan lebih banyak data sebelum memilih jadwal.'
    st.markdown(f'<div class="rec"><div class="rec-num">02 &nbsp; / &nbsp; WAKTU POSTING</div><div class="rec-title">{title}</div><div class="rec-text">{text}</div></div>',unsafe_allow_html=True)
with r3:
    small=agg[(agg.clicks<100)|(agg.orders<20)]
    title='Validasi sebelum scaling'; text=f'{len(small)} dari {len(agg)} jenis konten memiliki kurang dari 100 clicks atau 20 orders. Prioritaskan pengumpulan data dan evaluasi interval, bukan hanya peringkat.' if len(small) else 'Semua jenis konten mencapai 100 clicks dan 20 orders. Tetap uji perbedaan pada kampanye baru sebelum scaling.'
    st.markdown(f'<div class="rec"><div class="rec-num">03 &nbsp; / &nbsp; KUALITAS DATA</div><div class="rec-title">{title}</div><div class="rec-text">{text}</div></div>',unsafe_allow_html=True)

st.markdown('<div style="height:24px"></div>',unsafe_allow_html=True)
with st.expander('Metodologi & format data'):
    st.markdown('''**Format file:** satu baris per posting atau observasi kampanye. Kolom wajib: `tanggal`, `jenis_konten`, `clicks`, `orders`. Opsional: `channel`, `impressions`, `spend`, `revenue`, `jam` (0–23 atau HH:MM). Nama kolom umum berbahasa Inggris juga dikenali. Jika kolom opsional metrik tidak tersedia, nilainya dianggap 0. Untuk Excel, sheet pertama digunakan.

**Perhitungan:** conversion rate adalah total orders dibagi total clicks, bukan rata-rata persentase per baris. Interval kepercayaan 95% memakai metode Wilson untuk proporsi binomial. Insight utama memilih conversion rate tertinggi di antara jenis konten yang memenuhi ambang 100 clicks dan 20 orders; jika tidak ada yang memenuhi, ditampilkan peringkat tertinggi dengan peringatan. Angka nol clicks tidak dapat menghasilkan conversion rate. Rekomendasi waktu memakai ambang yang sama.

**Batasan:** hasil adalah asosiasi, tidak mengendalikan audiens, anggaran, promosi, atau faktor lain. Interval mengasumsikan setiap click independen dan satu click maksimal satu order; Perbandingan dua format menggunakan interval Newcombe untuk selisih dua proporsi, mengasumsikan kelompok dan clicks independen. Perbandingan dipilih setelah melihat data dan tidak dikoreksi untuk banyak pengujian, sehingga bersifat eksploratif. Angka demo adalah data sintetis, bukan performa nyata. Baris dengan angka kosong/negatif, tanggal tidak valid, atau orders lebih besar dari clicks akan diabaikan.''')
    st.download_button('↓ Unduh data terfilter (CSV)',df.to_csv(index=False).encode('utf-8-sig'),'vanguardia_data_terfilter.csv','text/csv')
st.markdown('<div style="text-align:center;margin-top:32px;color:#b1afbe;font-size:10px">VANGUARDIA &nbsp; · &nbsp; MAKE EVERY CAMPAIGN COUNT</div>',unsafe_allow_html=True)
