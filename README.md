# food-analysis

An in-depth analysis of food products from retail chain

<img src='https://github.com/grafstor/food-analysis/blob/main/media/penguin.gif?raw=true' align='center' width="200px">

## Product Price Prediction

I used **CatBoostRegressor** to build a regression model aimed at predicting product prices.

- **Root Mean Squared Error (RMSE) on the test set:** 274.3

#### Sample Predictions


|       | Product Name                                                                                 | Actual Price | Predicted Price |
| ----- | -------------------------------------------------------------------------------------------- | ------------ | --------------- |
| 2316  | Мёд Медовый Дом Крымские травы цветочный натур...    | 359.99       | 309.31          |
| 1121  | Горбуша натуральная Пр!ст, 250г                                       | 134.99       | 231.87          |
| 4560  | Масло сладкосливочное Традиционное несолёное 82%... | 219.99       | 213.23          |
| 11539 | Бренди Torres Гран Ресерва 10 38% в подарочной...                | 1849.00      | 2039.38         |
| 8664  | Хлеб Рижский Хлеб Ремесленный заварной из пшен...    | 91.99        | 80.77           |
| 5553  | Питахайя крупная                                                              | 479.99       | 210.93          |
| 7590  | Продукт растительный Kara Coconut Milk на осно...                   | 99.99        | 114.44          |
| 7953  | Маринад Костровок Идея на закуску для приготов...    | 75.99        | 111.53          |
| 2417  | Десерт Philosophia de Natura Яблочная карамель...                      | 159.99       | 191.99          |

## Grokking Experiment

In this experiment, I trained a **deep neural network** to explore the phenomenon of **grokking**, where, after extensive training, the model experiences a sudden surge in performance, even after overfitting has already occurred. To accelerate the training process, I utilized the **grokkfast** package, particularly the `gradfilter_ema` function, which optimized gradient updates.

For more information on **grokkfast**, visit the repository: [grokkfast GitHub](https://github.com/ironjr/grokfast).

#### Experiment Details

- **Epoch:** 749
- **Step:** 232,499
- **Training Loss:** 93,098.27
- **Minimum RMSE:** 405.57

#### Key Observations

- The model began overfitting after ~70 epochs.
- A dramatic performance improvement (grokking) was observed after ~700 epochs.

#### Hyperparameters

- **grokkfast: alpha:** 0.98
- **grokkfast: lambda:** 2.0
- **Learning rate (lr):** 3e-4
- **Weight decay:** 0.025
- **Hidden dimension (dim):** 128
- **Dropout:** 0.2

#### Experiment Graphs

![Frame 1](https://github.com/user-attachments/assets/967cd5b0-93aa-4ebb-97ac-180e620efc8b)

## Hypotheses Tested

During this project, several important questions were addressed through statistical analysis:

1. **Does the composition affect the product's rating?**

   **Method:** Regression analysis
   **Result:** 36 out of 128 p-values were less than the significance level ($\alpha$).
   **Conclusion:** The null hypothesis (H₀) is rejected, indicating that composition affects the product rating.
2. **Does the protein content depend on whether the product is sold by weight?**

   **Method:** T-test (non-normal distribution)
   **t-value:** 22.92
   **p-value:** $1.76 \times 10^{-88}$
   **Conclusion:** The null hypothesis (H₀) is rejected, meaning protein content depends on whether the product is sold by weight.
3. **Does the price depend on the shelf life?**

   **Method:** Spearman's correlation coefficient
   **Spearman’s coefficient:** 0.293
   **p-value:** $1.38 \times 10^{-243}$
   **Conclusion:** The null hypothesis (H₀) is rejected, showing that price depends on shelf life.
4. **Are foreign products more expensive?**

   **Method:** U-test
   **U-statistic:** 18,230,106
   **p-value:** $6.68 \times 10^{-278}$
   **Conclusion:** The null hypothesis (H₀) is rejected, indicating that foreign products are more expensive than local products.
5. **Is it true that discounts are less common for products with a short shelf life?**

   **Method:** U-test
   **U-statistic:** 17,661,316.5
   **p-value:** $2.39 \times 10^{-57}$
   **Conclusion:** The null hypothesis (H₀) is rejected. Contrary to the question, discounts are more common for products with a longer shelf life.
