import aiohttp
import random
from random import randint
from datetime import datetime, timedelta


class Pokemon:
    pokemonlar = {}

    def __init__(self, pokemon_egitmeni):
        self.pokemon_egitmeni = pokemon_egitmeni
        self.pokemon_numarasi = random.randint(1, 1000)
        self.isim = None
        self.img = None
        self.guc  = random.randint(30, 60)
        self.hp = random.randint(200, 400)
        self.son_besleme_zamani  = datetime.now()
        if pokemon_egitmeni  not in self.pokemonlar:
            self.pokemonlar[pokemon_egitmeni] = self

    async def besle(self, besleme_araligi=60, hp_artir=10):
        guncel_zaman  = datetime.now()
        delta_zaman  = timedelta(seconds=besleme_araligi)
        if (guncel_zaman - self.son_besleme_zamani) > delta_zaman:
            self.hp += hp_artir
            self.son_besleme_zamani = guncel_zaman
            return f"Pokémon'un sağlığı geri yüklenir. Mevcut HP: {self.hp}"
        else:
            return f"Pokémonunuzu şu zaman besleyebilirsiniz:{guncel_zaman -delta_zaman }"

    async def isim_al(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_numarasi}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['forms'][0]['name']
                else:
                    return "Pikachu"

    async def bilgi(self):
        if not self.isim:
            self.isim = await self.isim_al()
        return f"""Pokémon'un ismi: {self.isim}
                Pokémon'un gücü: {self.power}
                Pokémon'un sağlığı: {self.hp}"""

    async def resmi_goster(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_numarasi}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    resim_url = data['sprites']['front_default']
                    return resim_url   
                else:
                    return None

    async def saldir(self, dusman):
        if isinstance(dusman, Sihirbaz):
            sans = randint(1, 5)
            if sans == 1:
                return "Sihirbaz Pokémon, savaşta bir kalkan kullandı!"
        if dusman.hp > self.guc:
            dusman.hp -= self.guc
            return f"Pokémon eğitmeni @{self.pokemon_egitmeni} @{dusman.pokemon_egitmeni}'ne saldırdı\n@{dusman.pokemon_egitmeni}'nin sağlık durumu şimdi {dusman.hp}"
        else:
            dusman.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_egitmeni} @{dusman.pokemon_egitmeni}'ni yendi!"


class Sihirbaz(Pokemon):
    async def besle(self):
        return await super().besle(hp_artir=20)


class Dovuscu(Pokemon):
    async def saldir(self, dusman):
        super_guc  = randint(5, 15)
        self.guc  += super_guc 
        result = await super().saldir(dusman)
        self.guc -= super_guc
        return result + f"\nDovuscu Pokémon süper saldırı kullandı. Eklenen guc: {super_guc}"
    
    async def besle(self):
        return await super().besle(besleme_araligi=10)
