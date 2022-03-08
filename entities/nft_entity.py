class NFT:

    def __init__(self, nft_id=None, owner_id=None, nft_token=None, nft_url=None):
        self.nft_id, self.owner_id, self.nft_token, self.nft_url \
            = nft_id, owner_id, nft_token, nft_url

    def to_dict(self):
        return {
            "nft_id": self.nft_id,
            "owner_id": self.owner_id,
            "nft_token": self.nft_token,
            "nft_url": self.nft_url
        }

    def from_dict(self, dic):
        self.nft_id, self.owner_id, self.nft_token, self.nft_url \
            = dic['nft_id'], dic['owner_id'], dic['nft_token'], dic['nft_url']
