package com.example.recetasapp

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView

class RecetaAdapter(
    private val recetas: List<Receta>,
    private val onClick: (Receta) -> Unit
) : RecyclerView.Adapter<RecetaAdapter.RecetaViewHolder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecetaViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_receta, parent, false)
        return RecetaViewHolder(view)
    }

    override fun onBindViewHolder(holder: RecetaViewHolder, position: Int) {
        holder.bind(recetas[position])
    }

    override fun getItemCount(): Int = recetas.size

    inner class RecetaViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val nombre: TextView = itemView.findViewById(R.id.nombreReceta)
        private val descripcion: TextView = itemView.findViewById(R.id.descripcionReceta)
        private val imagen: ImageView = itemView.findViewById(R.id.imagenReceta)

        fun bind(receta: Receta) {
            nombre.text = receta.nombre
            descripcion.text = receta.descripcion
            imagen.setImageResource(receta.imagen)
            itemView.setOnClickListener { onClick(receta) }
        }
    }
}