# PN-ML-Challenge
The model parameters used in pipeline can be adjusted by changing **.env** file.

| **Variable**    | **Description**                 | **Example Value** |
|-----------------|---------------------------------|-------------------|
| TEST_SIZE       | How big the test size should be | 0.3               |

## Interactive commits
`make commit`

## How to create a new version of model?
Pipeline will always use a model with version specified in **VERSION** file.  
In case of making changes to a model update the recent version:
* `make bump` - will bump the version file of a model based on last commit created with commitizen  
* `make changelog UNRELEASED='cat VERSION'` - update changelog with recent commit history  
* `make all` - commit all files to repository

When a new version of a model will be created stages scripts will create new model file:  
*classifier/data/models/finalized_model-v0.1.0.sav*  
and a new score file:    
*classifier/data/scores/model-v0.1.0.txt*  
This value can be used to determine if a new model should be deployed or rollbacked.
