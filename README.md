## Библиотека pycades
Pycades реализует интерфейс аналогичный [CAdESCOM](https://docs.cryptopro.ru/cades/reference/cadescom).

Предназначена для встраивания криптографических операций в серверные приложения с использованием сертифицированного СКЗИ КриптоПро CSP.

Расширение предоставляет программный интерфейс, аналогичный КриптоПро ЭЦП Browser plug-in, для выполнения следующих криптографических операций:
-   работа с сертификатами;
-   создание и проверка подписи форматов CAdES BES, CAdES-T, CAdES-X Long Type 1;
-   шифрование и расшифрование данных.

### Особенности
В модуле pycades добавлены все константы из списка [свойств плагина](https://docs.cryptopro.ru/cades/plugin/plugin-methods?id=%d0%9a%d0%be%d0%bd%d1%81%d1%82%d0%b0%d0%bd%d1%82%d1%8b).

Для создания объектов необходимо вызвать соответствующий конструктор. Для создания доступны следующие объекты:

| Объект CAdESCOM |Объект pycades |
| :--- | :--- |
| CAdESCOM.About | pycades.About |
| CAdESCOM.CadesSignedData | pycades.SignedData |
| CAdESCOM.CPAttribute | pycades.Attribute |
| CAdESCOM.Certificate | pycades.Certificate |
| CAdESCOM.CRL | pycades.CRL |
| CAdESCOM.CPEnvelopedData | pycades.EnvelopedData |
| CAdESCOM.HashedData | pycades.HashedData |
| CAdESCOM.CPSigner | pycades.Signer |
| CAdESCOM.RawSignature | pycades.RawSignature |
| CAdESCOM.SignedXML | pycades.SignedXML |
| CAdESCOM.Store | pycades.Store |
| CAdESCOM.SymmetricAlgorithm | pycades.SymmetricAlgorithm |

### Установка библиотеки и примеры использования
[Сборка расширения](https://docs.cryptopro.ru/cades/pycades/pycades-build) и [установка библиотеки](https://docs.cryptopro.ru/cades/pycades/pycades-install).

[Примеры использования](https://docs.cryptopro.ru/cades/pycades/pycades-samples)

[Официальная документация](https://docs.cryptopro.ru/cades/pycades)
