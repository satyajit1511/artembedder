package com.example.myapplication;

import android.os.Bundle;
import android.widget.Button;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.myapplication.adapter.StudentAdapter;
import com.example.myapplication.db.DatabaseHelper;
import com.example.myapplication.model.User;
import com.google.android.material.textfield.TextInputEditText;

import java.util.List;

public class AddStudentActivity extends AppCompatActivity {

    private TextInputEditText etStudentName, etStudentRoll, etStudentPassword;
    private Button btnAddStudent;
    private RecyclerView rvStudents;
    private DatabaseHelper dbHelper;
    private StudentAdapter adapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_student);

        dbHelper = new DatabaseHelper(this);

        etStudentName = findViewById(R.id.etStudentName);
        etStudentRoll = findViewById(R.id.etStudentRoll);
        etStudentPassword = findViewById(R.id.etStudentPassword);
        btnAddStudent = findViewById(R.id.btnAddStudent);
        rvStudents = findViewById(R.id.rvStudents);

        rvStudents.setLayoutManager(new LinearLayoutManager(this));

        loadStudents();

        btnAddStudent.setOnClickListener(v -> {
            String name = etStudentName.getText() != null ? etStudentName.getText().toString().trim() : "";
            String roll = etStudentRoll.getText() != null ? etStudentRoll.getText().toString().trim() : "";
            String password = etStudentPassword.getText() != null ? etStudentPassword.getText().toString().trim() : "";

            if (name.isEmpty() || roll.isEmpty() || password.isEmpty()) {
                Toast.makeText(this, "Please fill all fields", Toast.LENGTH_SHORT).show();
                return;
            }

            boolean success = dbHelper.addStudent(roll, name, password);
            if (success) {
                Toast.makeText(this, "Student registered successfully!", Toast.LENGTH_SHORT).show();
                etStudentName.setText("");
                etStudentRoll.setText("");
                etStudentPassword.setText("");
                loadStudents();
            } else {
                Toast.makeText(this, "Failed to register student (Roll Number might already exist)", Toast.LENGTH_LONG).show();
            }
        });
    }

    private void loadStudents() {
        List<User> students = dbHelper.getAllStudents();
        adapter = new StudentAdapter(students, this::confirmDeleteStudent);
        rvStudents.setAdapter(adapter);
    }

    private void confirmDeleteStudent(User student) {
        new AlertDialog.Builder(this)
                .setTitle("Remove Student")
                .setMessage("Are you sure you want to remove " + student.getName() + " (Roll No: " + student.getUsername() + ") from the system?")
                .setPositiveButton("Remove", (dialog, which) -> {
                    boolean deleted = dbHelper.deleteStudent(student.getUsername());
                    if (deleted) {
                        Toast.makeText(this, "Student removed successfully", Toast.LENGTH_SHORT).show();
                        loadStudents();
                    } else {
                        Toast.makeText(this, "Failed to remove student", Toast.LENGTH_SHORT).show();
                    }
                })
                .setNegativeButton("Cancel", null)
                .show();
    }
}
