package com.example.myapplication;

import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.myapplication.db.DatabaseHelper;
import com.google.android.material.textfield.TextInputEditText;

public class RegisterTeacherActivity extends AppCompatActivity {

    private TextInputEditText etTeacherName, etTeacherUsername, etTeacherPassword, etTeacherConfirmPassword;
    private Button btnRegisterTeacher;
    private TextView tvBackToLogin;
    private DatabaseHelper dbHelper;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register_teacher);

        dbHelper = new DatabaseHelper(this);

        etTeacherName = findViewById(R.id.etTeacherName);
        etTeacherUsername = findViewById(R.id.etTeacherUsername);
        etTeacherPassword = findViewById(R.id.etTeacherPassword);
        etTeacherConfirmPassword = findViewById(R.id.etTeacherConfirmPassword);
        btnRegisterTeacher = findViewById(R.id.btnRegisterTeacher);
        tvBackToLogin = findViewById(R.id.tvBackToLogin);

        btnRegisterTeacher.setOnClickListener(v -> attemptTeacherRegistration());
        tvBackToLogin.setOnClickListener(v -> finish());
    }

    private void attemptTeacherRegistration() {
        String name = etTeacherName.getText() != null ? etTeacherName.getText().toString().trim() : "";
        String username = etTeacherUsername.getText() != null ? etTeacherUsername.getText().toString().trim() : "";
        String password = etTeacherPassword.getText() != null ? etTeacherPassword.getText().toString().trim() : "";
        String confirmPassword = etTeacherConfirmPassword.getText() != null ? etTeacherConfirmPassword.getText().toString().trim() : "";

        if (name.isEmpty() || username.isEmpty() || password.isEmpty() || confirmPassword.isEmpty()) {
            Toast.makeText(this, "Please fill in all fields", Toast.LENGTH_SHORT).show();
            return;
        }

        if (!password.equals(confirmPassword)) {
            Toast.makeText(this, "Passwords do not match!", Toast.LENGTH_SHORT).show();
            return;
        }

        boolean success = dbHelper.addTeacher(username, name, password);

        if (success) {
            Toast.makeText(this, "Teacher account created successfully! Please log in.", Toast.LENGTH_LONG).show();
            finish();
        } else {
            Toast.makeText(this, "Registration failed! Username/ID might already exist.", Toast.LENGTH_LONG).show();
        }
    }
}
