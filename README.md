# ESP32-Tool

### Descrição

ESP32 Tool é uma aplicação gráfica desenvolvida com Python e PyQt5 que facilita a configuração e geração de códigos de inicialização para os periféricos do ESP32. A ferramenta permite que você selecione os periféricos desejados para cada pino disponível e gera automaticamente o código de configuração correspondente em C para o framework ESP-IDF.

### Funcionalidades

- **Seleção intuitiva de periféricos para os pinos disponíveis no ESP32**.
- 
- **Suporte para diversos periféricos:**
    GPIO (Entrada e Saída)
    ADC (Conversor Analógico-Digital)
    DAC (Conversor Digital-Analógico)
    UART
    I2C (Master/Slave)
    SPI (Master/Slave)
    Touch Pad
    Opções de ativação para Wi-Fi, Bluetooth e BLE, etc.
    
- **Geração automática do código em C com:**
    Cabeçalho comentado.
    Inicialização dos periféricos selecionados.
    Exportação do código gerado como arquivo .c.
    Copiar código gerado para a área de transferência.

  ### Pré-requisitos

1. **Python 3.7+**
   - Instale o Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **Dependências Python**
   - Instale os pacotes necessários com:
     ```bash
     pip install -r requirements.txt
     ```

3. **ESP-IDF**
   - Configurado e instalado no seu ambiente de desenvolvimento.
   - Instruções: [Get Started with ESP-IDF](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/)

4. **Imagem ESP32**
   - Certifique-se de ter a imagem `esp32-wroom-32.png` no mesmo diretório do projeto.

### Como Usar

1. **Iniciar a aplicação**
   - Execute o arquivo principal:
     ```bash
     python esp32_tool.py
     ```

2. **Configurar os periféricos**
   - Insira o nome do projeto no campo de texto superior.
   - Selecione os periféricos desejados para cada pino utilizando os menus suspensos (ComboBoxes) à esquerda e à direita da interface.
   - Ative as opções de Wi-Fi, Bluetooth ou BLE, se necessário.

3. **Gerar o código**
   - Clique no botão **Generate Code**.
   - O código será exibido em uma nova janela.
   - Você pode copiá-lo para a área de transferência ou exportá-lo como arquivo `.c`.

4. **Compilar e carregar o código no ESP32**
   - Copie o código gerado para o arquivo `main.c` de um projeto ESP-IDF.
   - Compile o projeto:
     ```bash
     idf.py build
     ```
   - Carregue o código no ESP32:
     ```bash
     idf.py flash
     ```

