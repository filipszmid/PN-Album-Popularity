# PN-ML-Challenge


## Interactive commits
`make commit`

## How to create a new version of model?
* `make bump` - will bump the version file of a model based on last commit created with commitizen  
* `make changelog UNRELEASED='cat VERSION'` - update changelog with recent commit history  
* `make all` - commit all files to repository

When a new version of a model will be created stages scripts will create new model file:  
**classifier/data/models/finalized_model-v0.1.0.sav**  
and a new score file:    
**classifier/data/scores/model-v0.1.0.txt**
