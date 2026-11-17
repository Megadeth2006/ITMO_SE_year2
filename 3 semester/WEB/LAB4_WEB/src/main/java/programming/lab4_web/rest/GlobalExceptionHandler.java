package programming.lab4_web.rest;

import programming.lab4_web.dto.ErrorResponseDTO;
import programming.lab4_web.exceptions.AuthenticationException;
import programming.lab4_web.exceptions.DatabaseException;
import programming.lab4_web.exceptions.NotFoundException;
import programming.lab4_web.exceptions.ValidationException;

import javax.ws.rs.core.Response;
import javax.ws.rs.ext.ExceptionMapper;
import javax.ws.rs.ext.Provider;
import java.util.logging.Level;
import java.util.logging.Logger;

@Provider
public class GlobalExceptionHandler implements ExceptionMapper<Exception> {
    
    private static final Logger logger = Logger.getLogger(GlobalExceptionHandler.class.getName());
    
    @Override
    public Response toResponse(Exception exception) {
        logger.log(Level.SEVERE, "Exception caught by GlobalExceptionHandler", exception);
        
        if (exception instanceof AuthenticationException) {
            return handleAuthenticationException((AuthenticationException) exception);
        } else if (exception instanceof ValidationException) {
            return handleValidationException((ValidationException) exception);
        } else if (exception instanceof NotFoundException) {
            return handleNotFoundException((NotFoundException) exception);
        } else if (exception instanceof DatabaseException) {
            return handleDatabaseException((DatabaseException) exception);
        } else {
            return handleGenericException(exception);
        }
    }
    
    private Response handleAuthenticationException(AuthenticationException e) {
        ErrorResponseDTO error = new ErrorResponseDTO(
            "AUTHENTICATION_ERROR",
            e.getMessage()
        );
        return Response.status(Response.Status.UNAUTHORIZED)
                .entity(error)
                .build();
    }
    
    private Response handleValidationException(ValidationException e) {
        ErrorResponseDTO error = new ErrorResponseDTO(
            "VALIDATION_ERROR",
            e.getMessage()
        );
        return Response.status(Response.Status.BAD_REQUEST)
                .entity(error)
                .build();
    }
    
    private Response handleNotFoundException(NotFoundException e) {
        ErrorResponseDTO error = new ErrorResponseDTO(
            "NOT_FOUND",
            e.getMessage()
        );
        return Response.status(Response.Status.NOT_FOUND)
                .entity(error)
                .build();
    }
    
    private Response handleDatabaseException(DatabaseException e) {
        ErrorResponseDTO error = new ErrorResponseDTO(
            "DATABASE_ERROR",
            "Ошибка базы данных: " + e.getMessage()
        );
        logger.log(Level.SEVERE, "Database error occurred", e);
        return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                .entity(error)
                .build();
    }
    
    private Response handleGenericException(Exception e) {
        ErrorResponseDTO error = new ErrorResponseDTO(
            "INTERNAL_ERROR",
            "Внутренняя ошибка сервера: " + e.getMessage()
        );
        logger.log(Level.SEVERE, "Unexpected exception", e);
        return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                .entity(error)
                .build();
    }
}









