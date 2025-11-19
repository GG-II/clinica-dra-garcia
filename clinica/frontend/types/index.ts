export interface Usuario {
  id: number;
  username: string;
  email: string;
  nombres: string;
  apellidos: string;
  rol_id: number;
  activo: boolean;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface Rol {
  id: number;
  nombre: string;
  descripcion: string;
}