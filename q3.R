library(ggplot2)
library(pheatmap)

di = read.csv("/Users/giridhar.manoharan/Documents/data_incubator/COMPANY_SCORES_TOP_HALF.csv")
di$JUST_100 = as.numeric(di$JUST_100)
di$JUST_100 = di$JUST_100 - 1

View(di[3:10])
str(di[3:10])

pairs(di[c(3:14)])
pairs(di[c(23,27)])
#pheatmap(cor(di[c(3:37,39:50)], use="pairwise.complete.obs"))

###JUST_100 relationship with collective vairables
pheatmap(cor(di[3:14], use="pairwise.complete.obs"))
# JUST_100 more correlated with WGT_SCORE, TREAT and PAY

###JUST_100 with TREAT individual variables
pheatmap(cor(di[c(3,22:27)], use="pairwise.complete.obs"))
# some correlation between JUST_100 and TREAT.DISC, TREAT.RESPECT variables
pairs(di[c("TREAT.WLB","TREAT.RESPECT")]) ###linear correlation between TREAT.WLB and TREAT.RESPECT

###JUST_100 with PAY individual variables
pheatmap(cor(di[c(3,15:21)], use="pairwise.complete.obs"))
# correlation between JUST_100 and PAY.FAIR
# some correlation between JUST_100 and PAY.HEALTH, PAY.DISC, PAY.RETIRE

###JUST_100 with SUPPLY individual variables
pheatmap(cor(di[c(3,28:30)], use="pairwise.complete.obs")) # no meaningful correlation

###JUST_100 with COMM, JOBS, PROD, CUST individual variables
pheatmap(cor(di[c(3,31:37,39)], use="pairwise.complete.obs"))
# some correlation between JUST_100 and COMM.CHARITY
# correlation between COMM.CHARITY and PROD.BEN

###JUST_100 with LEAD, ENV, INVEST individual variables
pheatmap(cor(di[c(3,40:50)], use="pairwise.complete.obs")) #no meaningful correlation

### JUST_100 correlations putogether
pheatmap(cor(di[c("JUST_100", "TREAT", "PAY", "PAY.FAIR", "PAY.HEALTH", "PAY.DISC", "PAY.RETIRE", "TREAT.DISC", "TREAT.RESPECT", "COMM.CHARITY")], use="pairwise.complete.obs"), main = "HeatMap representing the correlation between JUST_100 (just score label) with other Metrics")

#plot(di$JUST_100 ~ di[,5], xlab=colnames(di)[4])

# ENSEMBLE MACHINE LEARNING - Random Forest
# To find important variables (features) that will have greater impact to the JUST_100 score
library(randomForest)
splitTrain <- function(data) {
  size <- nrow(data) * 0.9
  validation_index <- sample(1:nrow(data), size = size)
  validation <- data[-validation_index,]
  train <- data[validation_index,]
  return(list(train, validation))
}

trainRFModel <- function(train, num_trees) {
  set.seed(50)
  rf = randomForest(JUST_100~., data = train, importance = TRUE, ntree = num_trees)
  return(rf)
}

di$JUST_100 = as.factor(di$JUST_100)
data = splitTrain(di[3:ncol(di)])
train = data.frame(data[1])
test = data.frame(data[2])

rf = trainRFModel(train, 50)
predictions = predict(rf, test)
confusion.matrix = prop.table(table(predictions, test$JUST_100))
accuracy <- confusion.matrix[1,1] + confusion.matrix[2,2]
accuracy # 95.45% - high accuracy, so we can trust the variable importance plot results

#variable importance plot
par(mfrow=c(1,2))
varImpPlot(rf)