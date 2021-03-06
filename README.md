Networkx
========

Networkx, karmaşık ağları analiz ve manipüle etmek için geliştirilmiş bir Python kütüphanesidir. 

Karmaşık ağlara örnek olarak bilgisayar ağlarını ya da sosyal ağları örnek gösterebiliriz. 


Temel Graph Terimleri
=====================

Bir graph'ın temel yapısını oluşturan ve bir bilgisayarcının zaten hepsine aşina olduğu terimleri ve anlamlarını yazmak istiyorum.

Node (ya da Vertex)
-------------------

Bir graph'ın en temel parçasıdır. Bunu bir dictionary'inin bir key'i olarak düşünebilirsiniz. Bu key altında veri tutabilmekteyiz. Tutabildiğimiz bu verilere `Payload` demekteyiz.

Örnek: Bir sosyal ağ üzerindeki kişiler için node diyebiliriz.


Edge (Relationship)
-------------------

İki node arasındaki ilişkiye edge adını vermekteyiz. Node'larda olduğu gibi ilişkiler de veri tutabilir. İlişkiler tek yönlü ya da çift yönlü olabilir. İlişkileri tek yönlü olan bir graph'a `Directed Graph` deniyor.

İlişki yönlerini sosyal medya mecralarında gözlemleyebilirsiniz. Facebook üzerinde arkadaşınızla olan ilişkiniz graph üzerinde çift yönlüdür. Twitter üzerinde takip ettiğiniz biri ise tek yönlü.


Weight
------
Weight iki node arasındaki ilişkiyi niteleyen bir sayı değeridir. Bu sayı değeri uzaklık, maaliyet, ağırlık gibi değerler olabilir. Bir bilgisayar ağında `weight` değeri olarak kablo uzunluğu sayılabilir.


Path
----
İki node arasındaki bağlantının sağlanabilmesi için atlanması gereken node'ların dizisidir. Bir node üzerinden başka bir node'a en kısa şekilde ulaşabilmek için uğranılması gereken node'ları bulmak bir çözülebilir bir graph problemi olarak sayılabilir. Buna `shortest path` denir.

Sosyal ağ mecralarında bir kişiye ulaşabilmeniz için iletişime geçmeniz gereken kişilerin listesi örnek olarak verilebilir. Linkedin üzerine bir kişinin profilini incelediğinizde size kaçıncı dereceden bağlantınız olduğunu göstermektedir. Bu bağlantı sayısı en kısa yol (`sorthest path`) dizisinin eleman sayısıdır.

Degree
------
Bir node'un gelen ya da giden toplam bağlantı sayısıdır. Bir grup içindeki toplam bağlantı sayısı en yüksek olan node'a `hub` diyebiliriz.


Kolları Sıvayalım
=================
İnsanların birbirlerini takip edebildiği bir sosyal ağ düşünelim. Bunu en basit şekilde tasarlayacak olursak aşağıdaki gibi bir dictionary kullanabiliriz.

```python
network = {
    "fatih": ["erdem", "mehmetbarancay", "tayyiperdogdu", "cemal",
              "taylan", "yigit", "serkan", "tuna", "cihanokyay"],
    "cemal": ["taylan", "yigit", "serkan", "sinan"],
    "erdem": ["fatih", "yigit"],
    "taylan": ["yigit", "serkan", "tuna", "cemal"],
    "yigit": ["yigit", "serkan", "tuna", "can"],
    "serkan": ["yigit", "serkan", "tuna", "erdem"],
    "tuna": ["yigit", "taylan", "can"],
    "can": ["yigit", "serkan", "fatih", "sinan"],
    "sinan": ["yigit", "serkan", "fatih", "cemal"],
    "suatavni": ["tayyiperdogdu", "abdullahcicek", "mehmetbarancay"],
    "tayyiperdogdu": ["abdullahcicek", "suatavni", "feyzullahgulen"],
    "abdullahcicek": ["feyzullahgulen"],
    "feyzullahgulen": ["suatavni", "tayyiperdogdu", "suatavni"],
    "mehmetbarancay": ["suatavni", "feyzullahgulen"],
    "cihanokyay": ["fatihkadirakin", "sametatdag", "gokmengorgen"],
    "fatihkadirakin": ["cihanokyay", "berkerpeksag", "johnresig"],
    "sametatdag": ["cihanokyay", "fatihkadirakin", "berkerpeksag"],
    "berkerpeksag": ["cihanokyay", "gokmengorgen"],
    "gokmengorgen": ["cihanokyay", "sametatdag", "berkerpeksag"],
    "eminbugrasakal": ["eminbugrasakal"],
    "johnresig": ["douglescrockford", "addyosmani", "marijnhaverbeke"],
    "addyosmani": ["douglescrockford", "johnresig", "marijnhaverbeke"],
    "trevorburnham": ["douglescrockford", "johnresig", "marijnhaverbeke"],
    "marijnhaverbeke": ["douglescrockford", "addyosmani", "trevorburnham"],
    "douglescrockford": ["martinfowler", "trevorburnham"],
    "martinfowler": ["douglescrockford", "johnresig"],
}
```

Dictionary key'leri olarak kişiler ve değerleri olarak da o kişinin takip ettiği kişilerin listelerini tutuyoruz. Elimizdeki bu verileri networkx kütüphanesi ile üzerinde analiz yapabileceğimiz bir graph'a çevirebiliriz.

```python
import networkx as nx

# sosyal ağımız tek yönlü ilişkilerden oluşmaktadır.
# bu sebeple DirectedGraph kullanmalıyız.
graph = nx.DiGraph()

# ilk yapmamız gereken oluşturduğumuz graph'a nodları eklemek.
graph.add_nodes_from(network.keys())
for users in network.values():
    for user in users:
        if not user in graph:
            graph.add_node(user)

# node'lar üzerindeki ilişkileri (edge) tanımlıyoruz.
for user, followed_users in network.items():
    for followee in followed_users:
        graph.add_edge(user, followee)
```

Graph'ımızı oluşturduk. Bakalım nasıl gözüküyor.

```python
nx.draw(graph)
```

Elinizdeki graph'ı bir görsele çevirmek için `matplotlib` kütüphanesini kullanabilirsiniz. Ben IPython Notebook üzerinde çalışıyorum. Bu araç `nx.draw` metodunu çağırdığımda çıktıyı defterime yansıtıyor.

![graph](http://i.imgur.com/t8s0IUn.png "graph")

Yukarıda gördüğünüz garip şey oluşturduğumuz graph'ın çıktısıdır. Kırmızı daireler graph üzerindeki node'larımızı, aralarındaki bağlantılar ise edge'leri temsil etmektedir. Node ve edge arasındaki iki bıyık bükümlük kalın çizgi ise ilişkinin yönünü belirtmektedir.

Graph'ı incelediğimizde bazı node'ların yan yana kümeleştiğini farkediyoruz. Bu kümeleşmeleri bir sosyal ağ üzerindeki gruplaşmış kişiler ya da topluluklar olarak düşünebiliriz. Dikkat ederseniz kümeleşmeler birbiri arasında çok sık ilişkili. Kümeler içindeki bazı node'lar diğer kümelerle de ilişkili. 

Biraz daha somut örnek vermek istiyorum. Node'ları label'ları ile birlikte çizdireceğim.

![graph](http://i.imgur.com/K8n1ynn.png "graph")

Yukarıdaki görselde sağ altta oluşan kümeleşme bir topluluğu ifade ediyor. Bu topluluk Python İstanbul topluluğu. Bu veri topluluğun içerisindeki kişilerin birbirini takip etmesiyle ortaya çıktı.

Hadi bu graph üzerinde yorumladığımız kümelere erişmeye çalışalım. Bu kümeleşmeler birer subgraph olarak yorumlanabilir. Networkx size bir graph üzerine birbiriyle hiç bağlantısı olmayan node'ları, birbiriyle zayıf bağlantıları olanları, ya da birbiriyle bağlantıları güçlü olan node'ları subgraph olarak verebilir.

Biz birbirileriyle güçlü ilişkileri olan kümeleşmeleri istiyoruz. 

```python
>>> list(nx.strongly_connected_components(graph))
	[['johnresig',
	  'marijnhaverbeke',
	  'addyosmani',
	  'trevorburnham',
	  'douglescrockford',
	  'martinfowler'],
	 ['fatihkadirakin',
	  'cihanokyay',
	  'sametatdag',
	  'berkerpeksag',
	  'gokmengorgen'],
	 ['mehmetbarancay',
	  'suatavni',
	  'tayyiperdogdu',
	  'abdullahcicek',
	  'feyzullahgulen'],
	 ['fatih',
	  'cemal',
	  'taylan',
	  'tuna',
	  'can',
	  'sinan',
	  'serkan',
	  'erdem',
	  'yigit']]
```

Networkx güçlü bağlantılar için Tarjan's Algorithm algoritmasını kullanıyor. Bu algoritma bir directed graph'ın birbiriyle bağlantılı bileşenlerini çıkarmak için kullanılmakta. Bunun ile ilgili yeterince bilgiyi wikipedia'da bulabilirsiniz.

Elde ettiğimiz bu veriler ile graph üzerinde biraz uğraşalım. Örnek olarak her topluluğu farklı bir renkte gösterebiliriz.

```python
subgraphs = list(nx.strongly_connected_components(graph))

# html isimleri ile renklerimizi tanımlıyoruz
colors = ["lightgreen", "lemonchiffon", "skyblue", "mistyrose", "aliceblue"]


def find_color(node):
	# node'un dahil olduğu grup üzerinden rengini buluyoruz
    for subgraph in subgraphs:
        if node in subgraph:
            return colors[subgraphs.index(subgraph)]

    # node bir gruba değil değil
    return "ghostwhite"
    
node_colors = map(find_color, graph.nodes())

# çıktımızın görsel değerlerini belirleyip render ettiriyoruz
plt.figure(figsize=(16, 10))
nx.draw(graph, 
        with_labels=True, 
        node_size=1400, 
        node_color=node_colors, 
        width=0.3)
```

Aşağıdaki gibi bir çıktı elde etmekteyiz.

![graph](http://i.imgur.com/DLMkXXV.png "graph")

Bu gruplara isim vermek istiyorum.
	
	Mavi: Politikacılar
	Gülpembe: Hipo
	Sarı: Python İstanbul
	Yeşil: Javascript'çiler

Peki elimizdeki bu gruplar ve içindeki node'lar ile ne gibi problemler çözebiliriz? Tamamen sizin hayal gücünüze bağlı. 

Python İstanbul'daki birinin Hipo'dan birine mesaj göndermesi için iletişime geçmesi gereken kişilerin listesini çıkarabiliriz. 

Javascript grubundaki biri için takip edebileceği aynı gruptan yeni kişiler önerebiliriz.

Networkx hakkında bahsedeceklerim bu kadar, ancak içinde incelenecek dağlar kadar şey var. Kütüphanenin kaynak kodlarını mutlaka okumanızı tavsiye ediyorum.

Son olarak bahsettiğimiz problemleri bir graph database (neo4j gibi) üzerinde çözmeyi denemenizi önerebilirim. Çünkü günlük hayatta hesaplayıp bitireceğiniz graph'lardan ziyade anlık olarak üzerine çalışmamız ve scale etmeniz gereken senaryolar karşımıza çıkıyor.

Kolay gelsin.

- <http://networkx.github.io>
- <http://matplotlib.org>


