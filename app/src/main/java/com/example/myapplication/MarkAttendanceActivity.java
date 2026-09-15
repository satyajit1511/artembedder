package com.example.myapplication;

import android.app.DatePickerDialog;
import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.myapplication.adapter.AttendanceStudentAdapter;
import com.example.myapplication.db.DatabaseHelper;
import com.example.myapplication.model.Subject;
import com.example.myapplication.model.User;

import java.util.Calendar;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

public class MarkAttendanceActivity extends AppCompatActivity {

    private Spinner spinnerSubject;
    private TextView tvSelectedDate, tvAttendanceMode;
    private Button btnPickDate, btnSaveAttendance;
    private RecyclerView rvAttendanceStudents;
    private DatabaseHelper dbHelper;

    private List<Subject> subjectList;
    private List<User> studentList;
    private AttendanceStudentAdapter adapter;
    private String selectedDate;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_mark_attendance);

        dbHelper = new DatabaseHelper(this);

        spinnerSubject = findViewById(R.id.spinnerSubject);
        tvSelectedDate = findViewById(R.id.tvSelectedDate);
        tvAttendanceMode = findViewById(R.id.tvAttendanceMode);
        btnPickDate = findViewById(R.id.btnPickDate);
        btnSaveAttendance = findViewById(R.id.btnSaveAttendance);
        rvAttendanceStudents = findViewById(R.id.rvAttendanceStudents);

        rvAttendanceStudents.setLayoutManager(new LinearLayoutManager(this));

        // Set default date to today
        Calendar calendar = Calendar.getInstance();
        updateDateLabel(calendar.get(Calendar.YEAR), calendar.get(Calendar.MONTH), calendar.get(Calendar.DAY_OF_MONTH));

        btnPickDate.setOnClickListener(v -> {
            DatePickerDialog dialog = new DatePickerDialog(this, (view, year, month, dayOfMonth) -> {
                updateDateLabel(year, month, dayOfMonth);
            }, calendar.get(Calendar.YEAR), calendar.get(Calendar.MONTH), calendar.get(Calendar.DAY_OF_MONTH));
            dialog.show();
        });

        loadStudents();
        loadSubjects();

        spinnerSubject.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                loadExistingAttendance();
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {}
        });

        btnSaveAttendance.setOnClickListener(v -> saveAttendance());
    }

    private void updateDateLabel(int year, int month, int dayOfMonth) {
        selectedDate = String.format(Locale.getDefault(), "%04d-%02d-%02d", year, month + 1, dayOfMonth);
        tvSelectedDate.setText("Date: " + selectedDate);
        loadExistingAttendance();
    }

    private void loadSubjects() {
        subjectList = dbHelper.getAllSubjects();
        if (subjectList.isEmpty()) {
            Toast.makeText(this, "No subjects found! Please add subjects first.", Toast.LENGTH_LONG).show();
            return;
        }

        ArrayAdapter<Subject> spinnerAdapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item, subjectList);
        spinnerAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerSubject.setAdapter(spinnerAdapter);
        loadExistingAttendance();
    }

    private void loadStudents() {
        studentList = dbHelper.getAllStudents();
        if (studentList.isEmpty()) {
            Toast.makeText(this, "No students registered! Please add students first.", Toast.LENGTH_LONG).show();
            return;
        }

        adapter = new AttendanceStudentAdapter(studentList);
        rvAttendanceStudents.setAdapter(adapter);
    }

    private void loadExistingAttendance() {
        if (subjectList == null || subjectList.isEmpty() || spinnerSubject.getSelectedItem() == null || studentList == null || adapter == null) {
            return;
        }

        Subject selectedSubject = (Subject) spinnerSubject.getSelectedItem();
        boolean isAlreadyMarked = dbHelper.hasAttendanceRecord(selectedSubject.getId(), selectedDate);

        if (isAlreadyMarked) {
            tvAttendanceMode.setText("Editing Existing Record");
            tvAttendanceMode.setTextColor(Color.parseColor("#1976D2")); // Blue
        } else {
            tvAttendanceMode.setText("New Entry");
            tvAttendanceMode.setTextColor(Color.parseColor("#388E3C")); // Green
        }

        Map<String, String> existingMap = new HashMap<>();
        for (User student : studentList) {
            String status = dbHelper.getAttendanceStatus(student.getUsername(), selectedSubject.getId(), selectedDate);
            if (status != null) {
                existingMap.put(student.getUsername(), status);
            } else {
                existingMap.put(student.getUsername(), "PRESENT");
            }
        }

        adapter.setAttendanceMap(existingMap);
    }

    private void saveAttendance() {
        if (subjectList.isEmpty() || spinnerSubject.getSelectedItem() == null) {
            Toast.makeText(this, "Please select a valid subject", Toast.LENGTH_SHORT).show();
            return;
        }

        if (studentList.isEmpty() || adapter == null) {
            Toast.makeText(this, "No students to mark attendance for", Toast.LENGTH_SHORT).show();
            return;
        }

        Subject selectedSubject = (Subject) spinnerSubject.getSelectedItem();
        Map<String, String> attendanceMap = adapter.getAttendanceMap();

        boolean allSaved = true;
        for (User student : studentList) {
            String roll = student.getUsername();
            String status = attendanceMap.get(roll);
            if (status == null) status = "PRESENT";

            boolean success = dbHelper.markAttendance(roll, selectedSubject.getId(), selectedDate, status);
            if (!success) {
                allSaved = false;
            }
        }

        if (allSaved) {
            Toast.makeText(this, "Attendance updated successfully for " + selectedSubject.getSubjectName() + " (" + selectedDate + ")!", Toast.LENGTH_LONG).show();
            finish();
        } else {
            Toast.makeText(this, "Error saving attendance for some students", Toast.LENGTH_SHORT).show();
        }
    }
}
