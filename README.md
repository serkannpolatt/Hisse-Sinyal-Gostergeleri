## Türkçe
## Hisse Sinyal Göstergeleri

### Amaç:
Bu proje, belirli hisse senetlerinin piyasa verilerini analiz ederek alım-satım sinyalleri üretmek için geliştirilmiş bir araçtır. Kodlar, hisse senedi fiyatları ve çeşitli teknik göstergeler kullanılarak algoritmik olarak ticaret sinyalleri oluşturur.

### Kod Yapısı ve İşlevi:

- **Hisse_Temel_Verileri():** Belirli bir URL'den temel hisse verilerini çeker ve DataFrame'e dönüştürür.
- **TillsonT3():** Tillson T3 göstergesini hesaplar.
- **OTT():** OTT (Oscillator of Tillson) göstergesini hesaplar.
- **indicator_Signals():** Belirli bir hisse senedinin alım-satım sinyallerini üretmek için teknik göstergeleri kullanır.
- **st.sidebar:** Streamlit ile yan panel oluşturur ve hisse seçimi yapılmasını sağlar.
- **st.set_page_config():** Streamlit ile sayfa yapılandırmasını ayarlar.
- Göstergeleri yorumlar ve sonuçları kullanıcı arayüzünde gösterir.

### Kullanım:

1. Kodları çalıştırarak web arayüzünü açın.
2. Yan paneldeki hisse seçim kutusunu kullanarak analiz yapmak istediğiniz hisse senedini seçin.
3. Algoritma, seçilen hisse senedi için alım-satım sinyallerini hesaplar.
4. Sonuçları görüntülemek için metrikler ve veri tablosu kullanılabilir.

### Dikkat:

- Bu proje yalnızca eğitim amaçlı olup, gerçek ticaret kararları için profesyonel danışmanlık önerilir.

## English
## Stock Signal Indicators

### Aim:
This project is a tool developed to generate buying and selling signals by analyzing market data of specific stocks. The codes algorithmically generate trading signals using stock prices and various technical indicators.

### Code Structure and Function:

- **Stock_Basic_Data():** Pulls basic stock data from a given URL and converts it to DataFrame.
- **TillsonT3():** Calculates the Tillson T3 indicator.
- **OTT():** Calculates the OTT (Oscillator of Tillson) indicator.
- **indicator_Signals():** Uses technical indicators to generate buy-sell signals for a particular stock.
- **st.sidebar:** Creates a side panel with Streamlit and allows stock selection.
- **st.set_page_config():** Sets the page configuration with Streamlit.
- Interprets the indicators and displays the results in the user interface.

### Use:

1. Open the web interface by running the codes.
2. Select the stock you want to analyze using the stock selection box in the side panel.
3. The algorithm calculates buy-sell signals for the selected stock.
4. Metrics and data table can be used to display the results.

### Attention:

- This project is for educational purposes only, professional advice is recommended for real trading decisions.
