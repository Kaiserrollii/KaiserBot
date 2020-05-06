The following is a list of all the [WOEID](https://en.wikipedia.org/wiki/WOEID)s Twitter supports.
The `k.twitter_trends [Amount] [Location]` and `k.twitter_graph [Amount] [Location]` command(s) will work with any of these locations (467 total). 
When calling the command(s), DO NOT use the WOEID as the `[Location]` parameter; use the actual location itself (ex. `Worldwide`).

The `[Location]` parameter is not case sensitive because no one likes case sensitivity. However, you do have to get the spelling, 
spacing, and other special characters (ex. `Dallas-Ft. Worth`) right.

This list was formed by running api.trends_available and formatting it using the code below. 
The loop stopped numerous times throughout due to characters such as `ń`, `ó`, `Ú`, etc. Yeah, I'm looking at you, POLAND. Mexico too.

```
fout = open('WOEIDs.txt', 'w')
for i in api.trends_available():
    name = i['name']
    woeid = i['woeid']
    fout.write(f'{name}:{woeid}\n')
fout.close()
```


**Twitter-Supported WOEIDs - Full List**

```
Worldwide:1
Winnipeg:2972
Ottawa:3369
Quebec:3444
Montreal:3534
Toronto:4118
Edmonton:8676
Calgary:8775
Vancouver:9807
Birmingham:12723
Blackpool:12903
Bournemouth:13383
Brighton:13911
Bristol:13963
Cardiff:15127
Coventry:17044
Derby:18114
Edinburgh:19344
Glasgow:21125
Hull:25211
Leeds:26042
Leicester:26062
Liverpool:26734
Manchester:28218
Middlesbrough:28869
Newcastle:30079
Nottingham:30720
Plymouth:32185
Portsmouth:32452
Preston:32566
Sheffield:34503
Stoke-on-Trent:36240
Swansea:36758
London:44418
Belfast:44544
Santo Domingo:76456
Guatemala City:83123
Acapulco:110978
Aguascalientes:111579
Chihuahua:115958
Mexico City:116545
Ciudad Juarez:116556
Nezahualcoyotl:116564
Culiacan:117994
Ecatepec de Morelos:118466
Guadalajara:124162
Hermosillo:124785
Leon:131068
Merida:133327
Mexicali:133475
Monterrey:134047
Morelia:134091
Naucalpan de Juarez:134395
Puebla:137612
Queretaro:138045
Saltillo:141272
San Luis Potosi:144265
Tijuana:149361
Toluca:149769
Zapopan:151582
Mendoza:332471
Santiago:349859
Concepcion:349860
Valparaiso:349861
Bogota:368148
Cali:368149
Medellin:368150
Barranquilla:368151
Quito:375732
Guayaquil:375733
Caracas:395269
Maracaibo:395270
Maracay:395271
Valencia:395272
Barcelona:395273
Ciudad Guayana:395275
Turmero:395277
Lima:418440
Brasilia:455819
Belem:455820
Belo Horizonte:455821
Curitiba:455822
Porto Alegre:455823
Recife:455824
Rio de Janeiro:455825
Salvador:455826
Sao Paulo:455827
Campinas:455828
Fortaleza:455830
Goiania:455831
Manaus:455833
Sao Luis:455834
Guarulhos:455867
Cordoba:466861
Rosario:466862
Barquisimeto:468382
Maturin:468384
Buenos Aires:468739
Gdansk:493417
Krakow:502075
Lodz:505120
Poznan:514048
Warsaw:523920
Wroclaw:526363
Vienna:551801
Cork:560472
Dublin:560743
Galway:560912
Bordeaux:580778
Lille:608105
Lyon:609125
Marseille:610264
Montpellier:612977
Nantes:613858
Paris:615702
Rennes:619163
Strasbourg:627791
Toulouse:628886
Berlin:638242
Bremen:641142
Dortmund:645458
Dresden:645686
Dusseldorf:646099
Essen:648820
Frankfurt:650272
Hamburg:656958
Cologne:667931
Leipzig:671072
Munich:676757
Stuttgart:698064
Bologna:711080
Genoa:716085
Milan:718345
Naples:719258
Palermo:719846
Rome:721943
Turin:725003
Den Haag:726874
Amsterdam:727232
Rotterdam:733075
Utrecht:734047
Barcelona:753692
Bilbao:754542
Las Palmas:764814
Madrid:766273
Malaga:766356
Murcia:768026
Palma:769293
Seville:774508
Valencia:776688
Zaragoza:779063
Geneva:782538
Lausanne:783058
Zurich:784794
Brest:824382
Grodno:825848
Gomel:825978
Minsk:834463
Riga:854823
Bergen:857105
Oslo:862592
Gothenburg:890869
Stockholm:906057
Dnipropetrovsk:918981
Donetsk:919163
Kharkiv:922137
Kyiv:924938
Lviv:924943
Odesa:929398
Zaporozhye:939628
Athens:946738
Thessaloniki:963291
Bekasi:1030077
Depok:1032539
Pekanbaru:1040779
Surabaya:1044316
Makassar:1046138
Bandung:1047180
Jakarta:1047378
Medan:1047908
Palembang:1048059
Semarang:1048324
Tangerang:1048536
Singapore:1062617
Perth:1098081
Adelaide:1099805
Brisbane:1100661
Canberra:1100968
Darwin:1101597
Melbourne:1103816
Sydney:1105779
Kitakyushu:1110809
Saitama:1116753
Chiba:1117034
Fukuoka:1117099
Hamamatsu:1117155
Hiroshima:1117227
Kawasaki:1117502
Kobe:1117545
Kumamoto:1117605
Nagoya:1117817
Niigata:1117881
Sagamihara:1118072
Sapporo:1118108
Sendai:1118129
Takamatsu:1118285
Tokyo:1118370
Yokohama:1118550
Goyang:1130853
Yongin:1132094
Ansan:1132444
Bucheon:1132445
Busan:1132447
Changwon:1132449
Daegu:1132466
Gwangju:1132481
Incheon:1132496
Seongnam:1132559
Suwon:1132567
Ulsan:1132578
Seoul:1132599
Kajang:1141268
Ipoh:1154679
Johor Bahru:1154698
Klang:1154726
Kuala Lumpur:1154781
Calocan:1167715
Makati:1180689
Pasig:1187115
Taguig:1195098
Antipolo:1198785
Cagayan de Oro:1199002
Cebu City:1199079
Davao City:1199136
Manila:1199477
Quezon City:1199682
Zamboanga City:1199980
Bangkok:1225448
Hanoi:1236594
Hai Phong:1236690
Can Tho:1252351
Da Nang:1252376
Ho Chi Minh City:1252431
Algiers:1253079
Accra:1326075
Kumasi:1330595
Benin City:1387660
Ibadan:1393672
Kaduna:1396439
Kano:1396803
Lagos:1398823
Port Harcourt:1404447
Giza:1521643
Cairo:1521894
Alexandria:1522006
Mombasa:1528335
Nairobi:1528488
Durban:1580913
Johannesburg:1582504
Port Elizabeth:1586614
Pretoria:1586638
Soweto:1587677
Cape Town:1591691
Medina:1937801
Dammam:1939574
Riyadh:1939753
Jeddah:1939873
Mecca:1939897
Sharjah:1940119
Abu Dhabi:1940330
Dubai:1940345
Haifa:1967449
Tel Aviv:1968212
Jerusalem:1968222
Amman:1968902
Chelyabinsk:1997422
Khabarovsk:2018708
Krasnodar:2028717
Krasnoyarsk:2029043
Samara:2077746
Voronezh:2108210
Yekaterinburg:2112237
Irkutsk:2121040
Kazan:2121267
Moscow:2122265
Nizhny Novgorod:2122471
Novosibirsk:2122541
Omsk:2122641
Perm:2122814
Rostov-on-Don:2123177
Saint Petersburg:2123260
Ufa:2124045
Vladivostok:2124288
Volgograd:2124298
Karachi:2211096
Lahore:2211177
Multan:2211269
Rawalpindi:2211387
Faisalabad:2211574
Muscat:2268284
Nagpur:2282863
Lucknow:2295377
Kanpur:2295378
Patna:2295381
Ranchi:2295383
Kolkata:2295386
Srinagar:2295387
Amritsar:2295388
Jaipur:2295401
Ahmedabad:2295402
Rajkot:2295404
Surat:2295405
Bhopal:2295407
Indore:2295408
Thane:2295410
Mumbai:2295411
Pune:2295412
Hyderabad:2295414
Bangalore:2295420
Chennai:2295424
Mersin:2323778
Adana:2343678
Ankara:2343732
Antalya:2343733
Bursa:2343843
Diyarbakir:2343932
Eskisehir:2343980
Gaziantep:2343999
Istanbul:2344116
Izmir:2344117
Kayseri:2344174
Konya:2344210
Okinawa:2345896
Daejeon:2345975
Auckland:2348079
Albuquerque:2352824
Atlanta:2357024
Austin:2357536
Baltimore:2358820
Baton Rouge:2359991
Birmingham:2364559
Boston:2367105
Charlotte:2378426
Chicago:2379574
Cincinnati:2380358
Cleveland:2381475
Colorado Springs:2383489
Columbus:2383660
Dallas-Ft. Worth:2388929
Denver:2391279
Detroit:2391585
El Paso:2397816
Fresno:2407517
Greensboro:2414469
Harrisburg:2418046
Honolulu:2423945
Houston:2424766
Indianapolis:2427032
Jackson:2428184
Jacksonville:2428344
Kansas City:2430683
Las Vegas:2436704
Long Beach:2441472
Los Angeles:2442047
Louisville:2442327
Memphis:2449323
Mesa:2449808
Miami:2450022
Milwaukee:2451822
Minneapolis:2452078
Nashville:2457170
New Haven:2458410
New Orleans:2458833
New York:2459115
Norfolk:2460389
Oklahoma City:2464592
Omaha:2465512
Orlando:2466256
Philadelphia:2471217
Phoenix:2471390
Pittsburgh:2473224
Portland:2475687
Providence:2477058
Raleigh:2478307
Richmond:2480894
Sacramento:2486340
St. Louis:2486982
Salt Lake City:2487610
San Antonio:2487796
San Diego:2487889
San Francisco:2487956
San Jose:2488042
Seattle:2490383
Tallahassee:2503713
Tampa:2503863
Tucson:2508428
Virginia Beach:2512636
Washington:2514815
Osaka:15015370
Kyoto:15015372
Delhi:20070458
United Arab Emirates:23424738
Algeria:23424740
Argentina:23424747
Australia:23424748
Austria:23424750
Bahrain:23424753
Belgium:23424757
Belarus:23424765
Brazil:23424768
Canada:23424775
Chile:23424782
Colombia:23424787
Denmark:23424796
Dominican Republic:23424800
Ecuador:23424801
Egypt:23424802
Ireland:23424803
France:23424819
Ghana:23424824
Germany:23424829
Greece:23424833
Guatemala:23424834
Indonesia:23424846
India:23424848
Israel:23424852
Italy:23424853
Japan:23424856
Jordan:23424860
Kenya:23424863
Korea:23424868
Kuwait:23424870
Lebanon:23424873
Latvia:23424874
Oman:23424898
Mexico:23424900
Malaysia:23424901
Nigeria:23424908
Netherlands:23424909
Norway:23424910
New Zealand:23424916
Peru:23424919
Pakistan:23424922
Poland:23424923
Panama:23424924
Portugal:23424925
Qatar:23424930
Philippines:23424934
Puerto Rico:23424935
Russia:23424936
Saudi Arabia:23424938
South Africa:23424942
Singapore:23424948
Spain:23424950
Sweden:23424954
Switzerland:23424957
Thailand:23424960
Turkey:23424969
United Kingdom:23424975
Ukraine:23424976
United States:23424977
Venezuela:23424982
Vietnam:23424984
Petaling:56013632
Hulu Langat:56013645
Ahsa:56120136
Okayama:90036018
```
