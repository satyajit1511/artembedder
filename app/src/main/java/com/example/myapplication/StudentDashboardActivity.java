package com.example.myapplication;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.myapplication.adapter.StudentSummaryAdapter;
import com.example.myapplication.db.DatabaseHelper;
import com.example.myapplication.model.StudentAttendanceSummary;

import java.util.List;
import java.util.Locale;

public class StudentDashboardActivity extends AppCompatActivity {

    private TextView tvStudentNameHeader, tvStudentRollHeader, tvOverallPercentage, tvStatusBadge;
    private Button btnLogoutStudent;
    private RecyclerView rvSubjectSummary;
    private DatabaseHelper dbHelper;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_student_dashboard);

        dbHelper = new DatabaseHelper(this);

        tvStudentNameHeader = findViewById(R.id.tvStudentNameHeader);
        tvStudentRollHeader = findViewById(R.id.tvStudentRollHeader);
        tvOverallPercentage = findViewById(R.id.tvOverallPercentage);
        tvStatusBadge = findViewById(R.id.tvStatusBadge);
        btnLogoutStudent = findViewById(R.id.btnLogoutStudent);
        rvSubjectSummary = findViewById(R.id.rvSubjectSummary);

        rvSubjectSummary.setLayoutManager(new LinearLayoutManager(this));

        String studentRoll = getIntent().getStringExtra("STUDENT_ROLL");
        String studentName = getIntent().getStringExtra("STUDENT_NAME");

        if (studentName != null) {
            tvStudentNameHeader.setText(studentName);
        }
        if (studentRoll != null) {
            tvStudentRollHeader.setText("Roll No: " + studentRoll);
            loadStudentData(studentRoll);
        }

        btnLogoutStudent.setOnClickListener(v -> {
            Intent intent = new Intent(StudentDashboardActivity.this, LoginActivity.class);
            startActivity(intent);
            finish();
        });
    }

    private void loadStudentData(String studentRoll) {
        double overallPercentage = dbHelper.getStudentOverallPercentage(studentRoll);
        tvOverallPercentage.setText(String.format(Locale.getDefault(), "%.1f%%", overallPercentage));

        if (overallPercentage >= 75.0) {
            tvOverallPercentage.setTextColor(Color.parseColor("#2E7D32"));
            tvStatusBadge.setText("STATUS: ELIGIBLE (≥75%)");
            tvStatusBadge.setTextColor(Color.parseColor("#2E7D32"));
            tvStatusBadge.setBackgroundColor(Color.parseColor("#E8F5E9"));
        } else {
            tvOverallPercentage.setTextColor(Color.parseColor("#C62828"));
            tvStatusBadge.setText("STATUS: ATTENDANCE SHORTAGE (<75%)");
            tvStatusBadge.setTextColor(Color.parseColor("#C62828"));
            tvStatusBadge.setBackgroundColor(Color.parseColor("#FFEBEE"));
        }

        List<StudentAttendanceSummary> summaryList = dbHelper.getStudentAttendanceSummaries(studentRoll);
        StudentSummaryAdapter adapter = new StudentSummaryAdapter(summaryList);
        rvSubjectSummary.setAdapter(adapter);
    }
}
