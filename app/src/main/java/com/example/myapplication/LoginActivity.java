package com.example.myapplication;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.myapplication.db.DatabaseHelper;
import com.example.myapplication.model.User;
import com.google.android.material.textfield.TextInputEditText;
import com.google.android.material.textfield.TextInputLayout;

public class LoginActivity extends AppCompatActivity {

    private RadioGroup rgRole;
    private RadioButton rbTeacher, rbStudent;
    private TextInputLayout tilUsername;
    private TextInputEditText etUsername, etPassword;
    private Button btnLogin;
    private TextView tvRegisterTeacher;
    private DatabaseHelper dbHelper;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        dbHelper = new DatabaseHelper(this);

        rgRole = findViewById(R.id.rgRole);
        rbTeacher = findViewById(R.id.rbTeacher);
        rbStudent = findViewById(R.id.rbStudent);
        tilUsername = findViewById(R.id.tilUsername);
        etUsername = findViewById(R.id.etUsername);
        etPassword = findViewById(R.id.etPassword);
        btnLogin = findViewById(R.id.btnLogin);
        tvRegisterTeacher = findViewById(R.id.tvRegisterTeacher);

        rgRole.setOnCheckedChangeListener((group, checkedId) -> {
            if (checkedId == R.id.rbTeacher) {
                tilUsername.setHint("Teacher Username");
                tvRegisterTeacher.setVisibility(View.VISIBLE);
            } else {
                tilUsername.setHint("Student Roll Number");
                tvRegisterTeacher.setVisibility(View.GONE);
            }
        });

        btnLogin.setOnClickListener(v -> attemptLogin());
        tvRegisterTeacher.setOnClickListener(v -> startActivity(new Intent(LoginActivity.this, RegisterTeacherActivity.class)));
    }

    private void attemptLogin() {
        String username = etUsername.getText() != null ? etUsername.getText().toString().trim() : "";
        String password = etPassword.getText() != null ? etPassword.getText().toString().trim() : "";
        String role = rbTeacher.isChecked() ? "TEACHER" : "STUDENT";

        if (username.isEmpty()) {
            Toast.makeText(this, role.equals("TEACHER") ? "Please enter Username" : "Please enter Roll Number", Toast.LENGTH_SHORT).show();
            return;
        }

        if (password.isEmpty()) {
            Toast.makeText(this, "Please enter Password", Toast.LENGTH_SHORT).show();
            return;
        }

        User user = dbHelper.authenticateUser(username, password, role);

        if (user != null) {
            Toast.makeText(this, "Login Successful! Welcome " + user.getName(), Toast.LENGTH_SHORT).show();
            if ("TEACHER".equals(user.getRole())) {
                Intent intent = new Intent(LoginActivity.this, TeacherDashboardActivity.class);
                intent.putExtra("TEACHER_NAME", user.getName());
                startActivity(intent);
            } else {
                Intent intent = new Intent(LoginActivity.this, StudentDashboardActivity.class);
                intent.putExtra("STUDENT_ROLL", user.getUsername());
                intent.putExtra("STUDENT_NAME", user.getName());
                startActivity(intent);
            }
            finish();
        } else {
            Toast.makeText(this, "Invalid credentials or role. Please try again.", Toast.LENGTH_LONG).show();
        }
    }
}
