## Linear Discriminant Analysis (LDA) Visualization with Manim


The visualization of LDA includes a dataset with healthy and unhealthy classifications, 
a decision boundary created using LDA, and animations mapping data points to the decision boundary.


### 🛠 Installation
1. Clone the repository:
    ``` git clone https://github.com/AKayina/linear-discriminant-analysis.git ```

2. Navigate to the project directory:
    ``` cd linear-discriminant-analysis ```

3. Install dependencies:
    ``` pip install -r requirements.txt ```

4. Ensure the following Python libraries are installed:
    - ``` manim ```
    - ``` numpy ```
    - ``` scikit-learn ```

### 📋 Usage
To generate the animation:
    ``` manim -pql lda_visualization.py LDAPlot ```

### 🧰 Dependencies
  - Manim: Python animation engine
  - NumPy: For numerical operations
  - scikit-learn: For performing LDA
