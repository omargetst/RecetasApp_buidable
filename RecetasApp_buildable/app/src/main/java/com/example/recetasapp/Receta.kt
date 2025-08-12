package com.example.recetasapp

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

@Parcelize
data class Receta(
    val nombre: String,
    val descripcion: String,
    val imagen: Int,
    val etiquetas: List<String>,
    val porciones: Int,
    val tiempo: String,
    val carbs: String,
    val proteina: String,
    val grasa: String,
    val ingredientes: List<String>,
    val preparacion: List<String>
) : Parcelable