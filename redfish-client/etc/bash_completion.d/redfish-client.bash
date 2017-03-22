_redfish-client_complete_baseopts()
{
    case $2 in

        --help|-h)
            return 0
            ;;

    esac
    return 1
}
