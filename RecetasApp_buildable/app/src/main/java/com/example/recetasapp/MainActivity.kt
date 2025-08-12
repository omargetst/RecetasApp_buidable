package com.example.recetasapp

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val recetas = listOf(
            Receta(
                nombre = "Ensalada de aguacate y quinoa",
                descripcion = "Una ensalada fresca y nutritiva, perfecta para un almuerzo ligero.",
                imagen = R.drawable.ensaladaquinoa,
                etiquetas = listOf("Low Carb", "Quick"),
                porciones = 2,
                tiempo = "25 min",
                carbs = "350g",
                proteina = "20g",
                grasa = "12g",
                ingredientes = listOf("1 cup broccoli florets", "1 red bell pepper, sliced"),
                preparacion = listOf(
                    "En una sartén grande, calienta un poco de aceite a fuego medio-alto.",
                    "Agrega el brócoli y el pimiento, saltea por 5-7 minutos hasta que estén tiernos.",
                    "Sirve caliente."
                )
            ),
            Receta(
                nombre = "Lentejas Rojas",
                descripcion = "Tortillas rellenas de vegetales sazonados.",
                imagen = R.drawable.currylentejas,
                etiquetas = listOf("Low Carb", "Quick"),
                porciones = 4,
                tiempo = "20 min",
                carbs = "30g",
                proteina = "8g",
                grasa = "9g",
                ingredientes = listOf("Tortillas", "Pimientos", "Cebolla", "Tofu"),
                preparacion = listOf("Saltear vegetales", "Rellenar tortillas", "Servir"),

            ),
            Receta(
                nombre = "Tortilla Espinacas",
                descripcion = "Fresca y saludable, con aceite de oliva y queso feta.",
                imagen = R.drawable.tortillaespinacas,
                etiquetas = listOf("Low Carb", "Quick"),
                porciones = 2,
                tiempo = "10 min",
                carbs = "10g",
                proteina = "6g",
                grasa = "12g",
                ingredientes = listOf("Lechuga", "Tomate", "Aceitunas", "Queso feta", "Aceite de oliva"),
                preparacion = listOf("Cortar ingredientes", "Mezclar", "Añadir aderezo"),
            )
        )

        val recyclerView = findViewById<RecyclerView>(R.id.recyclerView)
        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = RecetaAdapter(recetas) { receta ->
            val intent = Intent(this, DetalleRecetaActivity::class.java)
            intent.putExtra("receta", receta)
            startActivity(intent)
        }
    }
}