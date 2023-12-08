from unittest import TestCase
from marvel import get_character_info, get_all_characters, get_shared_appearances, get_comic

class functionTestCase(TestCase):
    
    def test_get_character_info(self):
        self.assertEqual(get_character_info("Wolverine"), {'name': 'Wolverine', 'description': "Born with super-human senses and the power to heal from almost any wound, Wolverine was captured by a secret Canadian organization and given an unbreakable skeleton and claws. Treated like an animal, it took years for him to control himself. Now, he's a premiere member of both the X-Men and the Avengers.", 'image': 'http://i.annihil.us/u/prod/marvel/i/mg/2/60/537bcaef0f6cf/portrait_xlarge.jpg', 'wiki': 'http://marvel.com/comics/characters/1009718/wolverine?utm_campaign=apiRef&utm_source=3c53fc3b517b663bf6aabdf7db6177f5'})
        self.assertEqual(get_character_info("Magneto"), {'name': 'Magneto','description': '','image': 'http://i.annihil.us/u/prod/marvel/i/mg/3/b0/5261a7e53f827/portrait_xlarge.jpg','wiki': 'http://marvel.com/comics/characters/1009417/magneto?utm_campaign=apiRef&utm_source=3c53fc3b517b663bf6aabdf7db6177f5'} )


    def test_get_shared_appearances(self):
        self.assertIsNotNone(get_shared_appearances(1009718,1009417))
        self.assertIsNotNone(get_shared_appearances(1009268,1009351))

    