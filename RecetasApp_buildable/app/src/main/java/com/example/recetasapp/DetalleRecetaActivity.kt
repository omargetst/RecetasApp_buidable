package com.example.recetasapp

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class DetalleRecetaActivity : AppCompatActivity() {

    @SuppressLint("MissingInflatedId")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_detalle_receta)

        val receta = intent.getParcelableExtra<Receta>("receta") ?: return

        findViewById<ImageView>(R.id.imagenDetalle).setImageResource(receta.imagen)
        findViewById<TextView>(R.id.nombreDetalle).text = receta.nombre
        findViewById<TextView>(R.id.descripcionDetalle).text = receta.descripcion
        findViewById<TextView>(R.id.infoNutricional).text =
            "${receta.porciones} porciones | ${receta.tiempo} | ${receta.carbs} Carbs | ${receta.proteina} Protein | ${receta.grasa} Fat"
        findViewById<TextView>(R.id.ingredientesDetalle).text = receta.ingredientes.joinToString("\n")
        findViewById<TextView>(R.id.preparacionDetalle).text = receta.preparacion.joinToString("\n")

        // Botón de compartir
        findViewById<ImageView>(R.id.btnCompartir).setOnClickListener {
            val textoCompartir = """
                ${receta.nombre}
                ${receta.descripcion}
                
                Ingredientes:
                ${receta.ingredientes.joinToString("\n")}
                
                Preparación:
                ${receta.preparacion.joinToString("\n")}
            """.trimIndent()

            val intent = Intent().apply {
                action = Intent.ACTION_SEND
                putExtra(Intent.EXTRA_TEXT, textoCompartir)
                type = "text/plain"
            }

            startActivity(Intent.createChooser(intent, "Compartir receta vía"))
        }
    }
}
