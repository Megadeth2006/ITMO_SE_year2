package programming.lab4_web.dto;

import java.io.Serializable;
import java.time.LocalDateTime;

public class ErrorResponseDTO implements Serializable {
    private boolean success;
    private String error;
    private String message;
    private LocalDateTime timestamp;
    
    public ErrorResponseDTO() {
        this.timestamp = LocalDateTime.now();
    }
    
    public ErrorResponseDTO(String error, String message) {
        this.success = false;
        this.error = error;
        this.message = message;
        this.timestamp = LocalDateTime.now();
    }
    
    public boolean isSuccess() {
        return success;
    }
    
    public void setSuccess(boolean success) {
        this.success = success;
    }
    
    public String getError() {
        return error;
    }
    
    public void setError(String error) {
        this.error = error;
    }
    
    public String getMessage() {
        return message;
    }
    
    public void setMessage(String message) {
        this.message = message;
    }
    
    public LocalDateTime getTimestamp() {
        return timestamp;
    }
    
    public void setTimestamp(LocalDateTime timestamp) {
        this.timestamp = timestamp;
    }
}






