import unittest
from Bcoin import BlockChain


class TestBCoin(unittest.TestCase):

    def setUp(self):
        self.block_chain = BlockChain()

    def test_init(self):
        self.assertTrue(self.block_chain.chain)
        self.assertFalse(self.block_chain.current_transactions)
        self.assertFalse(self.block_chain.nodes)

    def test_new_block(self):
        block = self.block_chain.new_block('proof')
        self.assertEqual(block['proof'], 'proof')

    def test_new_transaction(self):
        transaction_block_index = self.block_chain.new_transaction('sender', 'recipient', 'amount')
        self.assertEqual(transaction_block_index, self.block_chain.last_block['index']+1)

    def test_proof_of_work(self):
        proof = self.block_chain.proof_of_work('1')
        self.assertTrue(self.block_chain.valid_proof('1', proof))

    def test_register_node(self):
        self.block_chain.register_node('http://127.0.0.1')
        self.assertTrue('127.0.0.1' in self.block_chain.nodes)

    def test_valid_chain(self):
        # 有效
        valid_block_chain = BlockChain()
        proof = valid_block_chain.proof_of_work(valid_block_chain.last_block['proof'])
        previous_hash = valid_block_chain.hash(valid_block_chain.last_block)
        valid_block_chain.new_block(proof, previous_hash)
        self.assertTrue(self.block_chain.valid_chain(valid_block_chain.chain))

        # previous_hash_error
        invalid_block_chain = BlockChain()
        proof = invalid_block_chain.proof_of_work(invalid_block_chain.last_block['proof'])
        invalid_block_chain.new_block(proof, 'previous_hash')
        self.assertFalse(self.block_chain.valid_chain(invalid_block_chain.chain))

        # Proof of work is not correct
        invalid_block_chain = BlockChain()
        previous_hash = invalid_block_chain.hash(invalid_block_chain.last_block)
        invalid_block_chain.new_block('proof', previous_hash)
        self.assertFalse(self.block_chain.valid_chain(invalid_block_chain.chain))

        # updated transactions on chain
        invalid_block_chain = BlockChain()
        proof = invalid_block_chain.proof_of_work(invalid_block_chain.last_block['proof'])
        previous_hash = invalid_block_chain.hash(invalid_block_chain.last_block)
        invalid_block_chain.new_block(proof, previous_hash)
        invalid_block_chain.chain[0]['transactions'].append({
            'sender': 'sender',
            'recipient': 'recipient',
            'amount': 'amount'
        })
        self.assertFalse(self.block_chain.valid_chain(invalid_block_chain.chain))
