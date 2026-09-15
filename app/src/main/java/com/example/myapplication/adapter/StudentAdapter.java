package com.example.myapplication.adapter;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.myapplication.R;
import com.example.myapplication.model.User;

import java.util.List;

public class StudentAdapter extends RecyclerView.Adapter<StudentAdapter.StudentViewHolder> {

    public interface OnStudentDeleteListener {
        void onDeleteClick(User student);
    }

    private final List<User> studentList;
    private final OnStudentDeleteListener deleteListener;

    public StudentAdapter(List<User> studentList, OnStudentDeleteListener deleteListener) {
        this.studentList = studentList;
        this.deleteListener = deleteListener;
    }

    @NonNull
    @Override
    public StudentViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_student, parent, false);
        return new StudentViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull StudentViewHolder holder, int position) {
        User student = studentList.get(position);
        holder.tvStudentName.setText(student.getName());
        holder.tvStudentRoll.setText("Roll No: " + student.getUsername());

        holder.btnDeleteStudent.setOnClickListener(v -> {
            if (deleteListener != null) {
                deleteListener.onDeleteClick(student);
            }
        });
    }

    @Override
    public int getItemCount() {
        return studentList.size();
    }

    static class StudentViewHolder extends RecyclerView.ViewHolder {
        TextView tvStudentName, tvStudentRoll;
        ImageButton btnDeleteStudent;

        public StudentViewHolder(@NonNull View itemView) {
            super(itemView);
            tvStudentName = itemView.findViewById(R.id.tvStudentName);
            tvStudentRoll = itemView.findViewById(R.id.tvStudentRoll);
            btnDeleteStudent = itemView.findViewById(R.id.btnDeleteStudent);
        }
    }
}
