import folium
from folium import ImageOverlay

# Criar o mapa centralizado em uma localização específica
m = folium.Map(location=[-23.55, -46.63], zoom_start=12)

# Definir os limites geográficos da imagem [sul-oeste, norte-leste]
bounds = [[-23.70, -46.80], [-23.40, -46.40]]

# Adicionar a imagem PNG como overlay
image_overlay = ImageOverlay(
    image='world.png',  # Caminho da imagem PNG
    bounds=bounds,
    opacity=0.6  # Define a opacidade da imagem
)

# Adicionar o overlay ao mapa
image_overlay.add_to(m)

# Exibir o mapa
m.save('map_with_overlay.html')
