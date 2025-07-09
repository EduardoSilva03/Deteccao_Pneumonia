import os
import numpy as np
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

# Configurações
BASE_DIR = "../../Images"
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 10
LR = 1e-4

# Geração e augmentação de imagens
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=20,
    zoom_range=0.15,
    horizontal_flip=True
)

train_gen = datagen.flow_from_directory(
    BASE_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='training'
)

val_gen = datagen.flow_from_directory(
    BASE_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='validation'
)

# Modelo com MobileNetV2
base = MobileNetV2(weights='imagenet', include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3))
base.trainable = False

x = GlobalAveragePooling2D()(base.output)
x = Dropout(0.3)(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.2)(x)
out = Dense(1, activation='sigmoid')(x)
model = Model(base.input, out)

model.compile(Adam(learning_rate=LR), loss='binary_crossentropy', metrics=['accuracy'])

# Treinamento com parada antecipada
stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
history = model.fit(train_gen, validation_data=val_gen, epochs=EPOCHS, callbacks=[stop])

# Avaliação
print(f"Acurácia: {model.evaluate(val_gen)[1]:.2f}")
print("\nRelatório:\n", classification_report(val_gen.classes, model.predict(val_gen) > 0.5))

# Salvar modelo
model.save("modelo_pneumonia.h5")

# Gráficos
plt.plot(history.history["accuracy"], label="Treino")
plt.plot(history.history["val_accuracy"], label="Validação")
plt.title("Acurácia")
plt.legend()
plt.show()