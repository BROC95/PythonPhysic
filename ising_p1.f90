! ! Introducción a la Simulación Computacional
! ! Edición: 2025
! ! Docentes: Joaquín Torres y Claudio Pastorino
! ! Estudiante: Breyner Ocampo Cárdenas
! ! Modelo de Ising 2D con Metropolis 
! ! Unidades reducidas kb=1, J=1 
! ! Proyecto 1: Simulación Monte Carlo térmico del Modelo de Ising. 
! ! Fecha de Entrega: Martes 14/10/2025

program ising_simulacion
    
  use ziggurat
  implicit none
  integer :: L, pasos, i, j, paso, aceptados
  real(8) :: kbT, beta, deltaE
  real(8), allocatable :: N(:,:)
  real(8) :: E_inst, M_inst, E_sum, M_sum, E2_sum, M2_sum
  real(8) :: E_sumT, M_sumT, E2_sumT, M2_sumT
  real(8) :: E_prom, M_prom, cv, chi, fraccion_aceptados
  real(8) :: err_E, err_M

  character(len=100) :: arg1
! 
    logical :: es, es2
    integer :: seed 
    real (kind=8) ::  p

integer :: pasos_termal , pasos_val


! Abrir archivos
  CALL GETARG(1, arg1)

  READ(arg1, *) kbT

  ! PRINT *, "Temperatura T=", kbT,  "kb= 1"


    inquire(file='input.dat',exist=es2)
    if(es2) then
        open(unit=11,file='input.dat',status='old')
        read(11,*) L
        close(11)
        ! print *,"  * Leyendo L de archivo input.dat " ,L
    else
        L = 30
    end if
    inquire(file='seed.dat',exist=es)
    if(es) then
        open(unit=10,file='seed.dat',status='old')
        read(10,*) seed
        close(10)
        ! print *,"  * Leyendo semilla de archivo seed.dat =", seed
    else
        seed = 24583490
    end if

    call zigset(seed)
  ! Leer temperatura desde línea de comandos
!   call getarg(1, arg1)
!   read(arg1, *) kbT
  beta = 1.0d0 / kbT
  ! print *, "Temperatura T =", kbT
  ! print *, "Temperatura L =", L

  ! Parámetros de simulación
!   L = 30
  pasos = 500000
  pasos_termal = pasos*0.20  ! por ejemplo, 20% de los pasos
pasos_val = pasos-pasos_termal
  aceptados = 0
  allocate(N(0:L+1, 0:L+1))
! print *,"Pasos de simulación: ",pasos
! print *,"Pasos de Termalización 20% : ",pasos_termal
  ! Inicializar spins aleatoriamente
  call inicializar_spines(N, L)

  ! Inicializar acumuladores
  E_sum = 0.0d0
  M_sum = 0.0d0
  E2_sum = 0.0d0
  M2_sum = 0.0d0
  ! E_inst =0 
  ! M_inst =0

  open(unit=22, file="Terma_U.csv", status='unknown')
open(unit=30, file="hist_E.csv", status='unknown')
open(unit=31, file="hist_M.csv", status='unknown')
  ! Bucle de Metropolis
write(22,*) "paso,E_prom_acum,M_prom_acum"
  do paso = 1, pasos
    i = int(uni() * L) + 1
    j = int(uni() * L) + 1

    deltaE = 2.0d0 * N(i,j) * (N(i+1,j) + N(i-1,j) + N(i,j+1) + N(i,j-1))

    if (deltaE <= 0.0d0 .or. uni() < exp(-deltaE / kbT)) then
      N(i,j) = -N(i,j)
      call actualizar_bordes(N, L)
      aceptados = aceptados + 1
    end if

write(30,*) E_inst
write(31,*) M_inst
    call calcular_energia(N, L, E_inst)
    call calcular_magnetizacion(N, L, M_inst)

    E_sum = E_sum + E_inst
    E2_sum = E2_sum + E_inst**2
    M_sum = M_sum + M_inst
    M2_sum = M2_sum + M_inst**2
    ! print * , E_sum, paso
! write(21,'(F6.2,",",I8)') E_sum, paso

! Calcular promedios acumulados hasta este paso
E_prom = E_sum / paso
M_prom = M_sum / paso

if ( paso .eq. pasos_termal )then
E2_sumT = E2_sum
E_sumT = E_sum
M2_sumT = M2_sum
M_sumT = M_sum
end if
! Guardar en archivo de termalización
write(22,'(I8,",",F12.6,",",F12.6)') paso, E_prom, M_prom

 
  end do
  close(22)
  close(30)
  close(31)

  ! Calcular observables
  E_sumT = E_sum-E_sumT
  ! E_prom = E_sum / pasos
  E_prom = E_sumT / pasos_val
  ! M_prom = M_sum / pasos
  M_sumT = M_sum-M_sumT
  M_prom = M_sumT / pasos_val
  E2_sumT = E2_sum-E2_sumT
  M2_sumT = M2_sum-M2_sumT
  cv = beta**2 / (L*L) * (E2_sumT/pasos_val - E_prom**2)
  chi = beta / (L*L) * (M2_sumT/pasos_val - M_prom**2)
  fraccion_aceptados = real(aceptados) / pasos
err_E = sqrt((E2_sumT/pasos_val - E_prom**2) / pasos_val)
err_M = sqrt((M2_sumT/pasos_val - M_prom**2) / pasos_val)

  ! Mostrar resultados
  ! print *, "⟨E⟩ =", E_prom
  ! print *, "⟨M⟩ =", M_prom
  ! print *, "c_v =", cv
  ! print *, "χ =", chi
  ! print *, "Fracción aceptada =", fraccion_aceptados
  ! print *, "Error Ener =", err_E
  ! print *, "Error Mag =", err_M

  ! Guardar en archivo CSV
  open(unit=20, file='observables.csv', status='unknown')
  write(20,*) "T,E_prom,M_prom,cv,chi,aceptados"
  write(20,'(F6.2,5(",",F12.6))') kbT, E_prom, M_prom, cv, chi, fraccion_aceptados
  close(20)
! call PrintMatrix(N,L)

open(unit=40, file="estado_final.csv", status="unknown")
do i = 1, L
  write(40,*) (N(i,j), j=1,L)
end do
close(40)

  deallocate(N)

  ! ! Escribir la última semilla para continuar con la cadena de numeros aleatorios 

        open(unit=10,file='seed.dat',status='unknown')
        seed = shr3() 
         write(10,*) seed
        close(10)
! ![FIN no Tocar]    
end program ising_simulacion

! Inicializa la matriz de spins aleatoriamente
subroutine inicializar_spines(N, L)
 use ziggurat
  integer, intent(in) :: L
  real(8), intent(out) :: N(0:L+1, 0:L+1)
  integer :: i, j
  do i = 1, L
    do j = 1, L
      if (uni() < 0.5d0) then
        N(i,j) = -1.0d0
      else
        N(i,j) = 1.0d0
      end if
    end do
  end do
  call actualizar_bordes(N, L)
end subroutine inicializar_spines

! Aplica condiciones de frontera periódicas
subroutine actualizar_bordes(N, L)
  integer, intent(in) :: L
  real(8), intent(inout) :: N(0:L+1, 0:L+1)
  N(0,:)     = N(L,:)
  N(:,0)     = N(:,L)
  N(L+1,:)   = N(1,:)
  N(:,L+1)   = N(:,1)
end subroutine actualizar_bordes

! Calcula la energía instantánea
! subroutine calcular_energia2(N, L, E)
!   integer, intent(in) :: L
!   real(8), intent(in) :: N(0:L+1, 0:L+1)
!   real(8), intent(out) :: E
!   integer :: i, j
!   E = 0.0d0
!   do i = 1, L
!     do j = 1, L
!       E = E - N(i,j) * (N(i+1,j) + N(i,j+1))
!     end do
!   end do
! end subroutine calcular_energia2
! Calcula la energía instantánea
subroutine calcular_energia(N, L, E)
  integer, intent(in) :: L
  real(8), intent(in) :: N(0:L+1, 0:L+1)
  real(8), intent(out) :: E
  integer :: i, j
  E = 0.0d0
do i = 1,L
    do j = 1, L
     E = E + N(i,j)*N(i+1,j)
     E = E + N(i,j)*N(i-1,j)
     E = E + N(i,j)*N(i,j+1)
     E = E + N(i,j)*N(i,j-1)
    end do
end do
E = E/2
end subroutine calcular_energia



subroutine calcular_magnetizacion(N, L, M)
  integer, intent(in) :: L
  real(8), intent(in) :: N(0:L+1, 0:L+1)
  real(8), intent(out) :: M
  integer :: i, j
  M = 0.0d0
  do i = 1, L
    do j = 1, L
      M = M + N(i,j)
    end do
  end do
end subroutine calcular_magnetizacion

SUBROUTINE PrintMatrix(M,L)
! Imprime una matriz cuadrada de tamaño (L+1)x(L+1)
real (kind=8) :: M(0:L+1,0:L+1)
CHARACTER(LEN=20) :: f
CHARACTER(LEN=5) :: num_str
WRITE(num_str, '(I0)') size(M, dim=2)
! Construir la cadena de formato
! L = L+2
f = '('// TRIM(num_str) //'F8.2)'
print *, "Formato de impresión: ", f
PRINT *, "Matriz:", size(M, dim=2)
PRINT *, "Matriz:", size(M, dim=1)
  DO i = 0, L+1
    !  write(*,f) (M(i,j), j=0,size(M, dim=1)-1)
     write(*,f) (M(i,j), j=0,L+1)
  END DO

RETURN
END