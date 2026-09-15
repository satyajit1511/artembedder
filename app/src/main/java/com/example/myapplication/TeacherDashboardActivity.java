package com.example.myapplication;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;

public class TeacherDashboardActivity extends AppCompatActivity {

    private TextView tvTeacherName;
    private Button btnLogout;
    private CardView cardAddStudent, cardAddSubject, cardMarkAttendance;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_teacher_dashboard);

        tvTeacherName = findViewById(R.id.tvTeacherName);
        btnLogout = findViewById(R.id.btnLogout);
        cardAddStudent = findViewById(R.id.cardAddStudent);
        cardAddSubject = findViewById(R.id.cardAddSubject);
        cardMarkAttendance = findViewById(R.id.cardMarkAttendance);

        String teacherName = getIntent().getStringExtra("TEACHER_NAME");
        if (teacherName != null && !teacherName.isEmpty()) {
            tvTeacherName.setText("Welcome, " + teacherName);
        }

        cardAddStudent.setOnClickListener(v -> startActivity(new Intent(TeacherDashboardActivity.this, AddStudentActivity.class)));
        cardAddSubject.setOnClickListener(v -> startActivity(new Intent(TeacherDashboardActivity.this, AddSubjectActivity.class)));
        cardMarkAttendance.setOnClickListener(v -> startActivity(new Intent(TeacherDashboardActivity.this, MarkAttendanceActivity.class)));

        btnLogout.setOnClickListener(v -> {
            Intent intent = new Intent(TeacherDashboardActivity.this, LoginActivity.class);
            startActivity(intent);
            finish();
        });
    }
}
