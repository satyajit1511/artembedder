package com.example.myapplication;

import android.os.Bundle;
import android.widget.Button;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.myapplication.adapter.SubjectAdapter;
import com.example.myapplication.db.DatabaseHelper;
import com.example.myapplication.model.Subject;
import com.google.android.material.textfield.TextInputEditText;

import java.util.List;

public class AddSubjectActivity extends AppCompatActivity {

    private TextInputEditText etSubjectName, etSubjectCode;
    private Button btnAddSubject;
    private RecyclerView rvSubjects;
    private DatabaseHelper dbHelper;
    private SubjectAdapter adapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_subject);

        dbHelper = new DatabaseHelper(this);

        etSubjectName = findViewById(R.id.etSubjectName);
        etSubjectCode = findViewById(R.id.etSubjectCode);
        btnAddSubject = findViewById(R.id.btnAddSubject);
        rvSubjects = findViewById(R.id.rvSubjects);

        rvSubjects.setLayoutManager(new LinearLayoutManager(this));

        loadSubjects();

        btnAddSubject.setOnClickListener(v -> {
            String name = etSubjectName.getText() != null ? etSubjectName.getText().toString().trim() : "";
            String code = etSubjectCode.getText() != null ? etSubjectCode.getText().toString().trim() : "";

            if (name.isEmpty() || code.isEmpty()) {
                Toast.makeText(this, "Please fill all fields", Toast.LENGTH_SHORT).show();
                return;
            }

            boolean success = dbHelper.addSubject(name, code);
            if (success) {
                Toast.makeText(this, "Subject added successfully!", Toast.LENGTH_SHORT).show();
                etSubjectName.setText("");
                etSubjectCode.setText("");
                loadSubjects();
            } else {
                Toast.makeText(this, "Failed to add subject", Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void loadSubjects() {
        List<Subject> subjects = dbHelper.getAllSubjects();
        adapter = new SubjectAdapter(subjects);
        rvSubjects.setAdapter(adapter);
    }
}
