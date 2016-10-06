
# ------------------------------------------------------------------------------
# Writing the validation code
# ------------------------------------------------------------------------------

# Dividing the set into training and validation set
    # Finding the places where R(i,j) == 1
i,j = np.where(R==1)
    # Randomly selecting 20% of the 1's
lengthij = shape(i)[0]
validateSize = int(round(0.2*lengthij))
randomIndex = random.sample(range(0,shape(i)[0]),validateSize)
    # Setting the randomly selected elements to 0
Rval = R
Rval[i[randomIndex],j[randomIndex]] = 0

# Doiong the training validation set
num_features = 1
regularization = 10
X, Theta =  ReccomenderSystem.collaberative_filtering(num_games,num_users,num_features,Rval,regularization)

# Checking precision, recall and correctness on the validation set
Predictions  = Theta * np.transpose(X)
shapeR = shape(R)
correctPositive = 0
falsePositive = 0
correctNegative = 0
falseNegative = 0
for i in range(0,shpeR[0]):
    for j in range(0,shapeR[1]):
        correct = R[i,j]
        prediction = round(Predictions[i,j])
        if correct == 1 and prediction == 1:
            correctPositive += 1
        if correct == 0 and prediction == 1:
            falsePositive += 1
        if correct == 0 and prediction == 0:
            correctNegative += 1
        if correct == 1 and prediction == 0:
            falseNegative += 1

precision = float(correctPositive)/(falsePositive + correctPositive)
recall = float(correctPositive)/(falseNegative + correctPositive)
correctness = float(correctPositive+correctNegative)/(correctPositive+correctNegative+falsePositive+falseNegative)
F_score = (2*precision[x]*recall[x])/(precision[x]+recall[x])
correctPositiveList = correctPositive
falsePositiveList = falsePositive
correctNegativeList = correctNegative
falseNegativeList = falseNegative

# ------------------------------------------------------------------------------
# Getting the correct value of lambda
# ------------------------------------------------------------------------------
# Checking the precision and recall for the trained model
lambdaList = [0, 0.1, 0.3, 0.7, 1, 3, 7, 10, 30, 70, 100, 300]

correctPositive = 0
falsePositive = 0
correctNegative = 0
falseNegative = 0

correctPositiveList = zeros(size(lambdaList))
falsePositiveList = zeros(size(lambdaList))
correctNegativeList = zeros(size(lambdaList))
falseNegativeList = zeros(size(lambdaList))
precision = zeros(size(lambdaList))
recall = zeros(size(lambdaList))
correctness = zeros(size(lambdaList))
F_score = zeros(size(lambdaList))

for x in range(0,size(lambdaList)):
    regularization = lambdaList[x]
    X, Theta =  ReccomenderSystem.collaberative_filtering(num_games,num_users,num_features,R,regularization)
    Predictions  = Theta * np.transpose(X)
    shapeR = shape(R)
    for i in range(0,shapeR[0]):
        for j in range(0,shapeR[1]):
            correct = R[i,j]
            prediction = round(Predictions[i,j])
            if correct == 1 and prediction == 1:
                correctPositive += 1
            if correct == 0 and prediction == 1:
                falsePositive += 1
            if correct == 0 and prediction == 0:
                correctNegative += 1
            if correct == 1 and prediction == 0:
                falseNegative += 1
    precision[x] = float(correctPositive)/(falsePositive + correctPositive)
    recall[x] = float(correctPositive)/(falseNegative + correctPositive)
    correctness[x] = float(correctPositive+correctNegative)/(correctPositive+correctNegative+falsePositive+falseNegative)
    F_score[x] = (2*precision[x]*recall[x])/(precision[x]+recall[x])
    correctPositiveList[x] = correctPositive
    falsePositiveList[x] = falsePositive
    correctNegativeList[x] = correctNegative
    falseNegativeList[x] = falseNegative


plt.plot(lambdaList,transpose(log10(correctPositiveList)),'-ob',label='Correct Positive')
plt.plot(lambdaList,transpose(log10(correctNegativeList)),'-or',label='Correct Negative')
plt.plot(lambdaList,transpose(log10(falsePositiveList)),'-xb',label='False Positive')
plt.plot(lambdaList,transpose(log10(falseNegativeList)),'-xr',label='False Negative')
plt.xlabel(r"$\lambda$ ",fontsize=16)
plt.ylabel('log #')

plt.legend()
fig = plt.gcf()
fig.savefig('correct_positive_negative.png', dpi=100, bbox_inches='tight')

plt.figure()
plt.plot(lambdaList,transpose(precision),'-ob',label='precision')
plt.plot(lambdaList,transpose(recall),'-or',label='recall')
plt.plot(lambdaList,transpose(correctness),'-ok',label='correctness')
plt.plot(lambdaList,F_score,'-om',label='F Score')

fig = plt.gcf()
plt.xlabel(r"$\lambda$ ",
          fontsize=16)
plt.legend()

fig.savefig('precision_recall.png', dpi=100, bbox_inches='tight')




# ------------------------------------------------------------------------------
# Showing the matrix
# ------------------------------------------------------------------------------
#plt.imshow(R[:,1000:2000])
#fig = plt.gcf()
#fig.set_size_inches(20, 20)
#fig.savefig('R.png', dpi=100, bbox_inches='tight')

#R2 = Theta * np.transpose(X)

#plt.imshow(R2[:,1000:2000])
#fig = plt.gcf()
#fig.set_size_inches(20, 20)
#fig.savefig('R*.png', dpi=100, bbox_inches='tight')

# ------------------------------------------------------------------------------
# Looking at the distribution of X and Theta
# ------------------------------------------------------------------------------
#hist_X = plt.hist(X,100)
#plt.show(hist_X)

#hist_Theta = plt.hist(Theta,100)
#plt.show(hist_Theta)
