program ising_simulacion
  use ziggurat
  implicit none

  integer :: L, pasos, i, j, paso, aceptados
  integer :: pasos_termal, pasos_val
  integer :: seed
  real(8) :: kbT, beta, deltaE
  real(8), allocatable :: N(:,:)
  real(8) :: E_inst, M_inst
  real(8) :: E_sum, M_sum, E2_sum, M2_sum
  real(8) :: E_sumT, M_sumT, E2_sumT, M2_sumT
  real(8) :: E_prom, M_prom, cv, chi, fraccion_aceptados
  real(8) :: err_E, err_M

  character(len=100) :: arg1
  logical :: es, es2

  ! --- Leer temperatura desde argumento de línea de comandos ---
  call getarg(1, arg1)
  read(arg1, *) kbT
  beta = 1.0d0 / kbT

  ! --- Leer L desde input.dat si existe ---
  inquire(file='input.dat', exist=es2)
  if (es2) then
    open(unit=11, file='input.dat', status='old', action='read')
    read(11, *) L
    close(11)
  else
    L = 30
  end if

  ! --- Leer semilla desde seed.dat si existe ---
  inquire(file='seed.dat', exist=es)
  if (es) then
    open(unit=10, file='seed.dat', status='old', action='read')
    read(10, *) seed
    close(10)
  else
    seed = 24583490
  end if
  call zigset(seed)

  ! --- Parámetros de simulación ---
  pasos = 500000
  pasos_termal = max(1, int(pasos * 0.20d0))   ! al menos 1 paso de termalización
  pasos_val = pasos - pasos_termal
  aceptados = 0

  allocate(N(0:L+1, 0:L+1))

  ! --- Inicializar spins aleatoriamente ---
  call inicializar_spines(N, L)

  ! --- Inicializar acumuladores ---
  E_sum = 0.0d0
  M_sum = 0.0d0
  E2_sum = 0.0d0
  M2_sum = 0.0d0
  E_sumT = 0.0d0
  M_sumT = 0.0d0
  E2_sumT = 0.0d0
  M2_sumT = 0.0d0

  ! --- Abrir archivos de salida ---
  open(unit=22, file="Terma_U.csv", status='unknown', action='write')
  open(unit=30, file="hist_E.csv", status='unknown', action='write')
  open(unit=31, file="hist_M.csv", status='unknown', action='write')

  write(22,*) "paso,E_prom_acum,M_prom_acum"

  ! --- Bucle de Metropolis ---
  do paso = 1, pasos
    ! elegir un sitio aleatorio (1..L)
    i = int( uni() * L ) + 1
    j = int( uni() * L ) + 1

    ! cambio de energía al invertir el spin (J = 1, Hamiltoniano H = - sum_{<ij>} s_i s_j)
    deltaE = 2.0d0 * N(i,j) * ( N(i+1,j) + N(i-1,j) + N(i,j+1) + N(i,j-1) )

    if ( deltaE <= 0.0d0 .or. uni() < exp( -deltaE * beta ) ) then
      N(i,j) = -N(i,j)
      call actualizar_bordes(N, L)
      aceptados = aceptados + 1
    end if

    ! calcular energía y magnetización instantáneas (por sitio)
    call calcular_energia(N, L, E_inst)       ! E_inst es la energía total
    call calcular_magnetizacion(N, L, M_inst) ! M_inst es magnetización total

    ! escribir histogramas instanteales (si se desea)
    write(30,*) E_inst
    write(31,*) abs(M_inst)

    ! acumular sumas (para promedios)
    E_sum = E_sum + E_inst
    E2_sum = E2_sum + E_inst**2
    M_sum = M_sum + M_inst
    M2_sum = M2_sum + M_inst**2

    ! promedios acumulados hasta este paso (útil para termalización)
    E_prom = E_sum / real(paso,8)
    M_prom = M_sum / real(paso,8)

    ! cuando termina la etapa de termalización guardo los acumuladores actuales
    if ( paso .eq. pasos_termal ) then
      E_sumT = E_sum
      E2_sumT = E2_sum
      M_sumT = M_sum
      M2_sumT = M2_sum
    end if

    write(22,'(I8,",",F12.6,",",F12.6)') paso, E_prom, M_prom

  end do

  close(22)
  close(30)
  close(31)

  ! --- Calcular observables finales (solo sobre pasos de medición) ---
  E_sumT = E_sum - E_sumT
  E2_sumT = E2_sum - E2_sumT
  M_sumT = M_sum - M_sumT
  M2_sumT = M2_sum - M2_sumT

  E_prom = E_sumT / real(pasos_val,8)
  M_prom = M_sumT / real(pasos_val,8)

  cv  = beta**2 / real(L*L,8) * (E2_sumT/real(pasos_val,8) - E_prom**2)
  chi = beta / real(L*L,8) * (M2_sumT/real(pasos_val,8) - M_prom**2)

  fraccion_aceptados = real(aceptados,8) / real(pasos,8)
  err_E = sqrt( (E2_sumT/real(pasos_val,8) - E_prom**2) / real(pasos_val,8) )
  err_M = sqrt( (M2_sumT/real(pasos_val,8) - M_prom**2) / real(pasos_val,8) )

  ! --- Guardar observables en CSV ---
  open(unit=20, file='observables.csv', status='unknown', action='write')
  write(20,*) "T,E_prom,M_prom,cv,chi,aceptados"
  write(20,'(F6.2,5(",",F12.6))') kbT, E_prom, M_prom, cv, chi, fraccion_aceptados
  close(20)

  ! --- Guardar estado final (matriz de spins) ---
  open(unit=40, file="estado_final.csv", status="unknown", action='write')
  do i = 1, L
    write(40,*) ( N(i,j), j = 1, L )
  end do
  close(40)

  deallocate(N)

  ! --- Escribir última semilla para continuar la cadena aleatoria ---
  open(unit=10, file='seed.dat', status='unknown', action='write')
  seed = shr3()
  write(10,*) seed
  close(10)

contains

  ! ------------------------------------------------------------------
  ! Subrutina: inicializar_spines
  ! ------------------------------------------------------------------
  subroutine inicializar_spines(N, L)
    use ziggurat
    implicit none
    integer, intent(in) :: L
    real(8), intent(out) :: N(0:L+1, 0:L+1)
    integer :: i, j

    do i = 1, L
      do j = 1, L
        if ( uni() < 0.5d0 ) then
          N(i,j) = -1.0d0
        else
          N(i,j) =  1.0d0
        end if
      end do
    end do

    call actualizar_bordes(N, L)
  end subroutine inicializar_spines

  ! ------------------------------------------------------------------
  ! Subrutina: actualizar_bordes (condiciones periódicas)
  ! ------------------------------------------------------------------
  subroutine actualizar_bordes(N, L)
    implicit none
    integer, intent(in) :: L
    real(8), intent(inout) :: N(0:L+1, 0:L+1)

    ! bordes horizontales
    N(0,1:L)     = N(L,1:L)
    N(L+1,1:L)   = N(1,1:L)

    ! bordes verticales
    N(1:L,0)     = N(1:L,L)
    N(1:L,L+1)   = N(1:L,1)

    ! esquinas (opcional, para completitud)
    N(0,0)       = N(L,L)
    N(0,L+1)     = N(L,1)
    N(L+1,0)     = N(1,L)
    N(L+1,L+1)   = N(1,1)
  end subroutine actualizar_bordes

  ! ------------------------------------------------------------------
  ! Subrutina: calcular_energia
  ! Devuelve la energía total del retículo con J = 1 y H = 0,
  ! usando H = - sum_{<ij>} s_i s_j  (cada par contado una vez).
  ! ------------------------------------------------------------------
  subroutine calcular_energia(N, L, E)
    implicit none
    integer, intent(in) :: L
    real(8), intent(in) :: N(0:L+1, 0:L+1)
    real(8), intent(out) :: E
    integer :: i, j

    E = 0.0d0
    do i = 1, L
      do j = 1, L
        ! sumar solo pares "derecha" y "arriba" para contar cada enlace una vez
        E = E - N(i,j) * ( N(i+1,j) + N(i,j+1) )
      end do
    end do
  end subroutine calcular_energia

  ! ------------------------------------------------------------------
  ! Subrutina: calcular_magnetizacion
  ! Devuelve la magnetización total (no dividida por N sitios)
  ! ------------------------------------------------------------------
  subroutine calcular_magnetizacion(N, L, M)
    implicit none
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

  ! ! ------------------------------------------------------------------
  ! ! Subrutina: PrintMatrix (útil para debug)
  ! ! ------------------------------------------------------------------
  ! subroutine PrintMatrix(M, L)
  !   implicit none
  !   integer, intent(in) :: L
  !   real(8), intent(in) :: M(0:L+1,0:L+1)
  !   integer :: i, j

  !   print *, "Matriz (0:" // trim(adjustl(itoa(L+1))) // ", 0:" // trim(adjustl(itoa(L+1))) // ")"
  !   do i = 0, L+1
  !     write(*,'(200(F6.1,1X))') ( M(i,j), j = 0, L+1 )
  !   end do
  ! contains
  !   function itoa(x) result(s)
  !     integer, intent(in) :: x
  !     character(len=12) :: s
  !     write(s,'(I0)') x
  !   end function itoa
  ! end subroutine PrintMatrix

end program ising_simulacion
