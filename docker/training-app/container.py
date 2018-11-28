from utils import Elasticsearch
from indexer import Indexer
from labeller import Labeller
from trainer import Trainer
from tester import Tester

es = Elasticsearch(timeout=30)
indexer = Indexer(es)
labeller = Labeller(es)
trainer = Trainer(es)
tester = Tester(es)
