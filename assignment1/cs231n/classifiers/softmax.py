from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    num_train = X.shape[0]
    num_class = W.shape[1]
    
    for i in range(num_train):
        scores = X[i].dot(W)
        correct_class_score = scores[y[i]]
        #为了防止数值不稳定性，减去max(scores)
        shift_scores = scores - np.max(scores)
        loss += -shift_scores[y[i]] + np.log(np.sum(np.exp(shift_scores)))
        
        for j in range(num_class):
            sofemax_variant= np.exp(shift_scores[j])/np.sum(np.exp(shift_scores))
            if j == y[i]:
                dW[:, j] += (-1+sofemax_variant)*X[i,:]
            else:
                dW[:, j] += sofemax_variant*X[i,:]
            
    data_loss = loss / num_train
    reg_loss = 0.5*reg*np.sum(W*W)
    loss = data_loss + reg_loss
                                              
    dW /= num_train
    dW += reg * W
    
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    num_train = X.shape[0]
    
    scores = np.dot(X,W)
    scores -= np.max(scores, axis=1, keepdims=True)
    scores_exp = np.exp(scores)
    probs = scores_exp / np.sum(scores_exp, axis=1, keepdims=True)
    
    correct_logloss = -np.log(probs[range(num_train), y])
    data_loss = np.sum(correct_logloss) / num_train 
    reg_loss = 0.5*reg*np.sum(W * W)
    loss = data_loss + reg_loss
    
    dscores = probs
    dscores[range(num_train), y] -= 1
    dscores /= num_train
    
    dW = np.dot(X.T, dscores)
    dW += reg*W
    


    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
